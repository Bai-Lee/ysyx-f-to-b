/* Included in io/map.c only when CONFIG_DTRACE is enabled. */
#ifdef CONFIG_DTRACE
#include <errno.h>
static FILE *c2_dtrace_file;
static uint64_t c2_dtrace_count, c2_dtrace_limit = 4096;
static int c2_dtrace_initialized;
static const char *c2_dtrace_filter;

static void c2_dtrace_close(void) {
  if (c2_dtrace_file) { fclose(c2_dtrace_file); c2_dtrace_file = NULL; }
}
static int c2_dtrace_selected(const char *name) {
  if (!c2_dtrace_filter || !*c2_dtrace_filter) return 1;
  const char *p=c2_dtrace_filter; size_t n=strlen(name);
  while (*p) {
    const char *end=strchr(p,','); size_t length=end ? (size_t)(end-p) : strlen(p);
    if (length==n && memcmp(p,name,n)==0) return 1;
    if (!end) break;
    p=end+1;
  }
  return 0;
}
static void c2_device_trace(IOMap *map, char op, paddr_t address, int length, word_t data) {
  if (!c2_dtrace_initialized) {
    c2_dtrace_initialized=1;
    const char *path=getenv("C_DTRACE_FILE"), *limit=getenv("C_DTRACE_LIMIT");
    c2_dtrace_filter=getenv("C_DTRACE_FILTER");
    if (limit) {
      char *end; errno=0; c2_dtrace_limit=strtoull(limit,&end,10);
      if (errno || end==limit || *end || *limit=='-') { fprintf(stderr,"DTRACE_CONFIG invalid limit\n"); exit(2); }
    }
    if (path && *path) {
      c2_dtrace_file=fopen(path,"w");
      if (!c2_dtrace_file) { perror("DTRACE_CONFIG open"); exit(2); }
      setvbuf(c2_dtrace_file,NULL,_IOLBF,0); atexit(c2_dtrace_close);
    }
  }
  if (!c2_dtrace_file || !c2_dtrace_selected(map->name)) return;
  if (c2_dtrace_count < c2_dtrace_limit)
    fprintf(c2_dtrace_file,"D pc=%08x op=%c map=%s addr=%08x len=%d data=%08x\n",cpu.pc,op,map->name,address,length,data);
  else if (c2_dtrace_count == c2_dtrace_limit)
    fprintf(c2_dtrace_file,"DTRACE_LIMIT limit=%" PRIu64 "\n",c2_dtrace_limit);
  if (c2_dtrace_count<=c2_dtrace_limit) c2_dtrace_count++;
}
#else
#define c2_device_trace(map,op,address,length,data) ((void)0)
#endif
