#include "game.h"
static int init(void *p){Map *m=p;const char *names[]={"Entry","Bridge","Treasure"};if(!Map_fill(m,names,3))return 0;m->owned[0]->east=m->owned[1];m->owned[1]->west=m->owned[0];m->owned[1]->east=m->owned[2];m->owned[2]->west=m->owned[1];return 1;}
Object MapProto={.init=init,.destroy=Map_destroy,.move=Map_move,.attack=Map_attack};
