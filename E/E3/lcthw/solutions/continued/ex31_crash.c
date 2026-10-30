#include <unistd.h>
int main(void){
    int i=0;
    while(i<10){
        usleep(3000);
        if(i==5){*(volatile int *)0=7;}
        ++i;
    }
    return 0;
}
