#ifndef B_CSR_H
#define B_CSR_H
#include <stdint.h>
#include <stdbool.h>
void c5_csr_reset(void);
bool b_csr_read(unsigned number, uint32_t *value, bool *readonly);
void b_csr_write(unsigned number, uint32_t value);
uint32_t b_mret(uint32_t pc);
void b_clock_tick(void);
void b_reference_clock(int reset);
#endif
