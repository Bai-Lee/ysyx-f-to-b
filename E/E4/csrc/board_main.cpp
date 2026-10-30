#include <nvboard.h>
#include "Vlab_board.h"
#include "verilated.h"
#include "semu.h"
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <unistd.h>
#include <poll.h>
#include <chrono>
void nvboard_bind_all_pins(Vlab_board*);
int main(int argc,char**argv){
    if(argc!=3)return 2;int mode=atoi(argv[1]);if(mode<0||mode>10)return 2;
    uint8_t memory[256];if(semu_load(argv[2],memory))return 3;
    VerilatedContext ctx;ctx.commandArgs(argc,argv);Vlab_board d{&ctx};d.mode=mode;
    nvboard_bind_all_pins(&d);nvboard_init();
    auto tick=[&](){d.clk=0;ctx.timeInc(20);d.eval();
      if(d.cpu_instruction!=memory[d.cpu_pc]){fprintf(stderr,"ROM mismatch pc=%u instruction=%u expected=%u\n",d.cpu_pc,d.cpu_instruction,memory[d.cpu_pc]);exit(1);}
      d.clk=1;ctx.timeInc(20);d.eval();};
    d.reset=1;for(int i=0;i<10;i++)tick();d.reset=0;
    auto start=std::chrono::steady_clock::now();uint64_t cycles=0;unsigned prev_sw=~0u,prev_led=~0u,prev_key=~0u,prev_active=~0u,prev_count=~0u,prev_mod=~0u,prev_pos=~0u;
    while(true){
        tick();nvboard_update();cycles++;
        unsigned mods=d.dbg_shift+2*d.dbg_ctrl;
        unsigned position=(d.dbg_x<<10)|d.dbg_y;
        if(d.sw!=prev_sw||d.led!=prev_led||d.dbg_key!=prev_key||d.dbg_active!=prev_active||d.dbg_count!=prev_count||mods!=prev_mod||(mode==8&&position!=prev_pos)){
            printf("STATE cycles=%llu mode=%d sw=%u led=%u key=%u ascii=%u active=%u count=%u mods=%u seg=%u,%u,%u,%u,%u,%u pc=%u x=%u y=%u dx=%u dy=%u\n",
                (unsigned long long)cycles,mode,d.sw,d.led,d.dbg_key,d.dbg_ascii,d.dbg_active,d.dbg_count,mods,d.seg0,d.seg1,d.seg2,d.seg3,d.seg4,d.seg5,d.cpu_pc,d.dbg_x,d.dbg_y,d.dbg_dx,d.dbg_dy);fflush(stdout);
            prev_sw=d.sw;prev_led=d.led;prev_key=d.dbg_key;prev_active=d.dbg_active;prev_count=d.dbg_count;prev_mod=mods;prev_pos=position;
        }
        if(cycles%4096==0){
            pollfd p{STDIN_FILENO,POLLIN,0};if(poll(&p,1,0)>0&&(p.revents&POLLIN)){char c;if(read(0,&c,1)==1&&c=='q')break;}
            if(std::chrono::steady_clock::now()-start>std::chrono::seconds(45))break;
        }
    }
    printf("BOARD_EXIT cycles=%llu pos=%u,%u directions=%u,%u\n",(unsigned long long)cycles,d.dbg_x,d.dbg_y,d.dbg_dx,d.dbg_dy);fflush(stdout);d.final();nvboard_quit();return 0;
}
