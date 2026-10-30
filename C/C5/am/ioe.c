#include <am.h>
#include <klib-macros.h>
#include <stdint.h>
#include "ps2.h"
#define UART ((volatile uint8_t *)0x10000000u)
#ifndef C5_GPU_FRAMEBUFFER
#define C5_GPU_FRAMEBUFFER ((volatile uint32_t *)0x21000000u)
#endif
bool ioe_init(void){return true;}
void ioe_read(int reg,void *buf) {
  switch(reg){
    case AM_TIMER_CONFIG:*(AM_TIMER_CONFIG_T*)buf=(AM_TIMER_CONFIG_T){.present=true,.has_rtc=false};break;
    case AM_TIMER_UPTIME:{
      volatile uint32_t *timer=(volatile uint32_t*)0x02000000u;
      uint32_t lo=timer[0],hi=timer[1];((AM_TIMER_UPTIME_T*)buf)->us=(((uint64_t)hi<<32)|lo)/100u;break;
    }
    case AM_TIMER_RTC:*(AM_TIMER_RTC_T*)buf=(AM_TIMER_RTC_T){.year=1900};break;
    case AM_UART_CONFIG:((AM_UART_CONFIG_T*)buf)->present=true;break;
    case AM_UART_RX:((AM_UART_RX_T*)buf)->data=(UART[5]&1)?UART[0]:-1;break;
    case AM_INPUT_CONFIG:((AM_INPUT_CONFIG_T*)buf)->present=true;break;
    case AM_INPUT_KEYBRD:keyboard_read(buf);break;
    case AM_GPU_CONFIG:*(AM_GPU_CONFIG_T*)buf=(AM_GPU_CONFIG_T){.present=true,.has_accel=false,.width=640,.height=480,.vmemsz=640*480*4};break;
    case AM_GPU_STATUS:((AM_GPU_STATUS_T*)buf)->ready=true;break;
    case AM_AUDIO_CONFIG:((AM_AUDIO_CONFIG_T*)buf)->present=false;break;
    default:panic("C5 IO register not implemented");
  }
}
void ioe_write(int reg,void *buf) {
  if(reg==AM_UART_TX){putch(((AM_UART_TX_T*)buf)->data);return;}
  if(reg==AM_GPU_FBDRAW){
    const AM_GPU_FBDRAW_T *draw=buf;const uint32_t *pixels=draw->pixels;
    const int width=draw->w,height=draw->h,x=draw->x,y=draw->y;
    if(!pixels||width<=0||height<=0||x>=640||y>=480||x<=-width||y<=-height)return;
    const int source_x=x<0?-x:0,source_y=y<0?-y:0;
    const int target_x=x<0?0:x,target_y=y<0?0:y;
    int copy_width=width-source_x,copy_height=height-source_y;
    if(copy_width>640-target_x)copy_width=640-target_x;
    if(copy_height>480-target_y)copy_height=480-target_y;
    const uint32_t *source=pixels+(size_t)source_y*width+source_x;
    volatile uint32_t *destination=C5_GPU_FRAMEBUFFER+target_y*640+target_x;
    for(int row=0;row<copy_height;row++){
      for(int column=0;column<copy_width;column++)destination[column]=source[column];
      source+=width;destination+=640;
    }
    return;
  }
  panic("C5 IO write not implemented");
}
