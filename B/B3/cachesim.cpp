#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>
#include <string>
#include <vector>
struct Line {bool valid=false,dirty=false;uint32_t tag=0;uint64_t age=0;};
struct Cache {
  unsigned lines,words,ways,sets,padding;bool data_cache;
  uint64_t accesses=0,misses=0,bypasses=0,reads=0,writes=0,writebacks=0,invalidations=0;
  std::vector<Line> entries;
  Cache(unsigned l,unsigned w,unsigned a,unsigned p,bool d):lines(l),words(w),ways(a),sets(l/a),padding(p),data_cache(d),entries(l){}
  static bool cached(uint32_t address){return (address>=0x30000000&&address<0x31000000)||(address>=0x80000000&&address<0x80400000)||(address>=0xa0000000&&address<0xa8000000);}
  void invalidate(){for(auto &line:entries)line.valid=false;invalidations++;}
  void access(uint32_t address,bool write) {
    accesses++;if(write)writes++;else reads++;
    if(!cached(address)){bypasses++;return;}
    if(!data_cache&&address>=0xa0000000&&address<0xa8000000)address+=padding;
    uint32_t block=address/(4*words),set=block%sets,tag=block/sets;
    unsigned first=set*ways,victim=first;
    for(unsigned w=0;w<ways;w++){
      auto&line=entries[first+w];
      if(line.valid&&line.tag==tag){line.age=accesses;line.dirty|=write;return;}
    }
    misses++;
    for(unsigned w=0;w<ways;w++){
      auto&line=entries[first+w];
      if(!line.valid){victim=first+w;break;}
      if(line.age<entries[victim].age)victim=first+w;
    }
    auto&line=entries[victim];if(line.valid&&line.dirty)writebacks++;
    line={true,write,tag,accesses};
  }
};
int main(int argc,char**argv) {
  try {
    std::string path;bool data=false,sweep=false;unsigned lines=16,words=1,ways=1,padding=0;
    for(int i=1;i<argc;i++){
      std::string a=argv[i];auto v=[&](){if(++i>=argc)throw std::runtime_error("MISSING_ARGUMENT");return std::string(argv[i]);};
      if(a=="--trace")path=v();else if(a=="--data")data=true;else if(a=="--sweep")sweep=true;
      else if(a=="--lines")lines=std::stoul(v());else if(a=="--words")words=std::stoul(v());
      else if(a=="--ways")ways=std::stoul(v());else if(a=="--padding")padding=std::stoul(v());else throw std::runtime_error("UNKNOWN_ARGUMENT");
    }
    auto power=[](unsigned n){return n&&!(n&(n-1));};
    if(path.empty()||!power(lines)||!power(words)||!power(ways)||ways>lines||padding%4)throw std::runtime_error("CACHE_PARAMETERS");
    std::vector<Cache> caches;
    if(sweep){for(unsigned capacity:{64u,128u,256u,512u,1024u})for(unsigned block:{1u,4u,8u})for(unsigned assoc:{1u,2u,4u})if(capacity/(4*block)>=assoc)caches.emplace_back(capacity/(4*block),block,assoc,padding,data);}
    else caches.emplace_back(lines,words,ways,padding,data);
    FILE*stream=std::fopen(path.c_str(),"rb");if(!stream)throw std::runtime_error("TRACE_OPEN");
    uint64_t records=0;uint32_t item[5];
    for(;;){size_t n=std::fread(item,1,sizeof item,stream);if(n==0){if(std::ferror(stream))throw std::runtime_error("TRACE_READ");break;}if(n!=sizeof item)throw std::runtime_error("TRUNCATED_TRACE");records++;
      if(item[4]&~3u)throw std::runtime_error("TRACE_FLAGS");
      for(auto&cache:caches){
        if(data){if(item[4]&1)cache.access(item[3],item[4]&2);}
        else {cache.access(item[0],false);if((item[1]&0x707f)==0x100f)cache.invalidate();}
      }
    }
    std::fclose(stream);
    std::printf("{\"records\":%llu,\"data_cache\":%s,\"replacement\":\"LRU\",\"write_policy\":\"%s\",\"configs\":[",(unsigned long long)records,data?"true":"false",data?"write-back write-allocate estimate":"read-only instruction");
    for(size_t i=0;i<caches.size();i++){const auto&c=caches[i];if(i)std::printf(",");
      std::printf("{\"lines\":%u,\"words\":%u,\"ways\":%u,\"padding\":%u,\"capacity_bytes\":%u,\"accesses\":%llu,\"misses\":%llu,\"bypasses\":%llu,\"reads\":%llu,\"writes\":%llu,\"writebacks\":%llu,\"invalidations\":%llu}",c.lines,c.words,c.ways,c.padding,c.lines*c.words*4,(unsigned long long)c.accesses,(unsigned long long)c.misses,(unsigned long long)c.bypasses,(unsigned long long)c.reads,(unsigned long long)c.writes,(unsigned long long)c.writebacks,(unsigned long long)c.invalidations);
    }
    std::printf("]}\n");return 0;
  }catch(const std::exception&e){std::fprintf(stderr,"CACHESIM_REJECT %s\n",e.what());return 2;}
}
