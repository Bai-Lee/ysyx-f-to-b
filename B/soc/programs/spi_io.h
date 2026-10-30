#ifndef C5_SPI_IO_H
#define C5_SPI_IO_H
#include <stdint.h>
#define SPI_REG ((volatile uint32_t*)0x10001000u)
#define SPI_GO (1u<<8)
#define SPI_ASS (1u<<13)
#define SPI_TX_NEG (1u<<10)
static inline uint32_t spi_transfer(unsigned slave,unsigned bits,uint32_t low,uint32_t high) {
  while(SPI_REG[4]&SPI_GO){}
  uint32_t config=SPI_ASS|SPI_TX_NEG|(bits&127);
  SPI_REG[4]=config;
  SPI_REG[0]=low;SPI_REG[1]=high;
  SPI_REG[5]=0;
  SPI_REG[6]=1u<<slave;
  SPI_REG[4]=config|SPI_GO;
  while(SPI_REG[4]&SPI_GO){}
  return SPI_REG[0];
}
static inline uint32_t flash_read(uint32_t offset) {
  uint32_t value=spi_transfer(0,64,0,0x03000000u|(offset&0x00ffffffu));
  return ((value>>24)&255)|((value>>8)&0xff00)|((value<<8)&0xff0000)|(value<<24);
}
#endif
