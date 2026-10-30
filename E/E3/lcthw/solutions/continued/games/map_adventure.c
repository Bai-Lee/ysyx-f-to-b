#include "game.h"
static int init(void *p){Map *m=p;const char *names[]={"Hall","Throne","Arena","Kitchen","Garden","Tower"};if(!Map_fill(m,names,6))return 0;
Room **r=m->owned;r[0]->north=r[1];r[1]->south=r[0];r[1]->west=r[2];r[2]->east=r[1];r[1]->east=r[3];r[3]->west=r[1];r[3]->north=r[4];r[4]->south=r[3];r[4]->east=r[5];r[5]->west=r[4];
for(int i=0;i<3;i++){int index=(int[]){2,4,5}[i];r[index]->bad_guy=NEW(Monster,"guard");if(!r[index]->bad_guy)return 0;}return 1;}
Object MapProto={.init=init,.destroy=Map_destroy,.move=Map_move,.attack=Map_attack};
