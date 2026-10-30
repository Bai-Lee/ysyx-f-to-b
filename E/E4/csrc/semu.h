#ifndef E4_SEMU_H
#define E4_SEMU_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct {uint8_t pc,r[4],led,display;int enhanced;} Semu;
void semu_reset(Semu *s,int enhanced);
void semu_step(Semu *s,uint8_t instruction,uint8_t switches,uint8_t buttons);
int semu_load(const char *path,uint8_t memory[256]);
#ifdef __cplusplus
}
#endif
#endif
