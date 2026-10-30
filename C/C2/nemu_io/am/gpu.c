/* C2 IOE implementation; framebuffer is row-major 00RRGGBB. */
#include <am.h>
#include <nemu.h>
#include <klib.h>
#include <klib-macros.h>

#define SYNC_ADDR (VGACTL_ADDR + 4)

void __am_gpu_init(void) {}

void __am_gpu_config(AM_GPU_CONFIG_T *cfg) {
  uint32_t dimensions = inl(VGACTL_ADDR);
  *cfg = (AM_GPU_CONFIG_T) {
    .present = true, .has_accel = false,
    .width = dimensions >> 16, .height = dimensions & 0xffff,
    .vmemsz = (dimensions >> 16) * (dimensions & 0xffff) * sizeof(uint32_t)
  };
}

void __am_gpu_fbdraw(AM_GPU_FBDRAW_T *ctl) {
  uint32_t dimensions = inl(VGACTL_ADDR);
  int sw = dimensions >> 16, sh = dimensions & 0xffff;
  assert(ctl->w >= 0 && ctl->h >= 0);
  if (ctl->w && ctl->h) {
    assert(ctl->pixels != NULL);
    /* Clip the destination, retaining the original source row stride. */
    int64_t x0 = ctl->x, y0 = ctl->y;
    int64_t x1 = x0 + ctl->w, y1 = y0 + ctl->h;
    if (x0 < 0) x0 = 0;
    if (y0 < 0) y0 = 0;
    if (x1 > sw) x1 = sw;
    if (y1 > sh) y1 = sh;
    volatile uint32_t *fb = (volatile uint32_t *)(uintptr_t)FB_ADDR;
    const uint32_t *pixels = ctl->pixels;
    for (int64_t y = y0; y < y1; y++)
      for (int64_t x = x0; x < x1; x++)
        fb[(size_t)y * sw + (size_t)x] = pixels[(size_t)(y - ctl->y) * (size_t)ctl->w + (size_t)(x - ctl->x)];
  }
  if (ctl->sync) outl(SYNC_ADDR, 1);
}

void __am_gpu_status(AM_GPU_STATUS_T *status) { status->ready = true; }
