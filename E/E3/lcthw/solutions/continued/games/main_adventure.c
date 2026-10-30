#include <stdio.h>
#include <stdlib.h>
#include "game.h"
int main(void){srand(260719);Map *m=NEW(Map,"Adventure");if(!m)return 1;m->location->proto.describe(m->location);int ch;
while((ch=getchar())!=EOF&&ch!='q'){if(ch=='n')m->proto.move(m,NORTH);else if(ch=='s')m->proto.move(m,SOUTH);else if(ch=='e')m->proto.move(m,EAST);else if(ch=='w')m->proto.move(m,WEST);else if(ch=='a')m->proto.attack(m,1+rand()%4);else if(ch=='l')m->location->proto.describe(m->location);}
m->proto.destroy(m);return 0;}
