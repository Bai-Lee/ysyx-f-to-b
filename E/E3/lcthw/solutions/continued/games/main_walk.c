#include <stdio.h>
#include "game.h"
int main(void){Map *m=NEW(Map,"Walk");if(!m)return 1;m->location->proto.describe(m->location);m->proto.move(m,EAST);m->proto.move(m,EAST);puts("treasure reached");m->proto.destroy(m);return 0;}
