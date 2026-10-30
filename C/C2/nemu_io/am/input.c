#include <am.h>
#include <nemu.h>

#define KEYDOWN_MASK 0x8000u

void __am_input_keybrd(AM_INPUT_KEYBRD_T *kbd) {
  uint32_t value = inl(KBD_ADDR);
  kbd->keydown = (value & KEYDOWN_MASK) != 0;
  kbd->keycode = value & ~KEYDOWN_MASK;
}
