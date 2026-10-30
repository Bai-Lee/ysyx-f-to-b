#include <am.h>
#include <klib.h>
#include <stdint.h>
#define read_csr(name) ({uint32_t value;__asm__ volatile("csrr %0," #name:"=r"(value));value;})
#define write_csr(name,value) __asm__ volatile("csrw " #name ",%0"::"r"((uint32_t)(value)):"memory")
#define check(condition) do{if(!(condition))halt(60);}while(0)
extern void c5_test_trap(void);
extern char c5_ecall_site;
int main(const char *args) {
  (void)args;
  check(read_csr(mvendorid)==0x79737978u&&read_csr(marchid)==0x26070001u&&read_csr(mhartid)==0);
  const uint32_t values[]={0,1,0xffffffff,0x12345678,0x80000000,0xa5a55a5a};
  uint32_t expected=0;
  for(unsigned i=0;i<sizeof(values)/sizeof(values[0]);i++){
    uint32_t old,value=values[i];
    __asm__ volatile("csrrw %0,mscratch,%1":"=r"(old):"r"(value):"memory");check(old==expected);expected=value;
    check(read_csr(mscratch)==expected);
    value=0x01010101;
    __asm__ volatile("csrrs %0,mscratch,%1":"=r"(old):"r"(value):"memory");check(old==expected);expected|=value;
    value=0x00ff00ff;
    __asm__ volatile("csrrc %0,mscratch,%1":"=r"(old):"r"(value):"memory");check(old==expected);expected&=~value;
    check(read_csr(mscratch)==expected);
  }
  uint32_t old;
  __asm__ volatile("csrrwi %0,mscratch,31":"=r"(old)::"memory");check(old==expected&&read_csr(mscratch)==31);
  __asm__ volatile("csrrci %0,mscratch,15":"=r"(old)::"memory");check(old==31&&read_csr(mscratch)==16);
  __asm__ volatile("csrrsi %0,mscratch,3":"=r"(old)::"memory");check(old==16&&read_csr(mscratch)==19);
  __asm__ volatile("csrrsi zero,mscratch,0":::"memory");check(read_csr(mscratch)==19);
  register uint32_t collision __asm__("a0")=0x89abcdef;
  __asm__ volatile("csrrw a0,mscratch,a0":"+r"(collision)::"memory");check(collision==19&&read_csr(mscratch)==0x89abcdef);
  write_csr(mstatus,0xffffffff);check(read_csr(mstatus)==0x1888);
  write_csr(mepc,0x1234567b);check(read_csr(mepc)==0x12345678);
  write_csr(mtvec,(uintptr_t)c5_test_trap|3);check(read_csr(mtvec)==(uintptr_t)c5_test_trap);
  write_csr(mtvec,(uintptr_t)c5_test_trap|1);check(read_csr(mtvec)==((uintptr_t)c5_test_trap|1));
  write_csr(mstatus,0x1808);
  for(unsigned i=0;i<4;i++){
    register uint32_t marker __asm__("t2");
    __asm__ volatile(".balign 4\n.globl c5_ecall_site\nc5_ecall_site: ecall":"=r"(marker)::"t0","t1","memory");
    check(marker==123&&read_csr(mcause)==11&&read_csr(mepc)==(uintptr_t)&c5_ecall_site+4&&read_csr(mstatus)==0x1888);
  }
  printf("CSR/TRAP PASS project=%08x\n",read_csr(marchid));
  return 0;
}
