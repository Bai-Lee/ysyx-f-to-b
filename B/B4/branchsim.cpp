#include <cstdint>
#include <cstdio>
#include <stdexcept>
#include <string>
static uint32_t sext(uint32_t n,unsigned bits){uint32_t s=1u<<(bits-1);return (n^s)-s;}
int main(int argc,char**argv){
  try{
    if(argc!=2)throw std::runtime_error("TRACE_REQUIRED");FILE*f=std::fopen(argv[1],"rb");if(!f)throw std::runtime_error("TRACE_OPEN");
    uint64_t instructions=0,branches=0,jal=0,jalr=0,returns=0,nt=0,taken=0,btfnt=0,degenerate=0;
    uint32_t r[5];
    for(;;){size_t n=std::fread(r,1,sizeof r,f);if(!n){if(std::ferror(f))throw std::runtime_error("TRACE_READ");break;}if(n!=sizeof r)throw std::runtime_error("TRUNCATED_TRACE");instructions++;
      uint32_t pc=r[0],i=r[1],next=r[2];unsigned opcode=i&127;
      if(opcode==0x63){
        uint32_t imm=sext(((i>>31)<<12)|(((i>>7)&1)<<11)|(((i>>25)&63)<<5)|(((i>>8)&15)<<1),13),target=pc+imm;
        if(next!=pc+4&&next!=target)throw std::runtime_error("BRANCH_TARGET_INVALID");branches++;nt+=next==pc+4;taken+=next==target;btfnt+=next==((i>>31)?target:pc+4);degenerate+=target==pc+4;
      }else if(opcode==0x6f){
        uint32_t imm=sext(((i>>31)<<20)|(((i>>12)&255)<<12)|(((i>>20)&1)<<11)|(((i>>21)&1023)<<1),21);
        if(next!=pc+imm)throw std::runtime_error("JAL_TARGET_INVALID");jal++;
      }else if(opcode==0x67){jalr++;returns+=((i>>7)&31)==0&&((i>>15)&31)==1&&(i>>20)==0;}
    }
    std::fclose(f);if(!instructions)throw std::runtime_error("EMPTY_TRACE");
    std::printf("{\"instructions\":%llu,\"conditional_branches\":%llu,\"jal\":%llu,\"jalr\":%llu,\"returns\":%llu,\"correct_next_pc\":{\"always_not_taken\":%llu,\"always_taken\":%llu,\"backward_taken\":%llu},\"same_target_as_fallthrough\":%llu,\"branch_fraction\":%.12f,\"ideal_scenarios\":[",(unsigned long long)instructions,(unsigned long long)branches,(unsigned long long)jal,(unsigned long long)jalr,(unsigned long long)returns,(unsigned long long)nt,(unsigned long long)taken,(unsigned long long)btfnt,(unsigned long long)degenerate,double(branches)/instructions);
    bool first=true;for(double accuracy:{1.,.995,.99,.95,.9,.8}){
      double miss=double(branches)/instructions*(1-accuracy);if(!first)std::printf(",");first=false;
      std::printf("{\"accuracy\":%.4f,\"five_stage_single_ipc\":%.9f,\"fifteen_stage_single_ipc\":%.9f,\"fifteen_stage_four_issue_ipc\":%.9f}",accuracy,1/(1+2*miss),1/(1+12*miss),1/(.25+12*miss));
    }
    std::printf("]}\n");return 0;
  }catch(const std::exception&e){std::fprintf(stderr,"BRANCHSIM_REJECT %s\n",e.what());return 2;}
}
