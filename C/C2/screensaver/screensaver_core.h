#ifndef C_SCREEN_CORE_H
#define C_SCREEN_CORE_H
#include <stdint.h>
#include <stdbool.h>
#ifndef assert
#include <assert.h>
#endif

/* Quantize the exact nonnegative linear interpolation by rounding downward. */
static inline uint32_t screen_blend(uint32_t from, uint32_t to,
                                    unsigned step, unsigned total) {
  assert(total && step <= total && total <= 1000000);
  uint32_t color = 0;
  for (unsigned shift = 0; shift <= 16; shift += 8) {
    unsigned a = (from >> shift) & 255u, b = (to >> shift) & 255u;
    unsigned channel = (a * (total - step) + b * step) / total;
    color |= channel << shift;
  }
#ifdef SCREEN_BAD_BLEND
  color ^= 1u;
#endif
  return color;
}

typedef struct { uint8_t down[256]; unsigned held; } screen_keys;
static inline void screen_key(screen_keys *keys, unsigned key, bool down) {
  if (!key || key >= 256) return;
  if (down && !keys->down[key]) { keys->down[key] = 1; keys->held++; }
  if (!down && keys->down[key]) { keys->down[key] = 0; keys->held--; }
}
#endif
