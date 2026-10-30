#include <stdio.h>
#include <stdlib.h>
#include "game.h"
static int Monster_init(void *p){((Monster *)p)->hit_points=10;return 1;}
static int Monster_attack(void *p,int damage){Monster *m=p;m->hit_points-=damage;if(m->hit_points<=0){puts("dead");return 1;}puts("alive");return 0;}
Object MonsterProto={.init=Monster_init,.attack=Monster_attack};
static void Room_destroy(void *p){Room *r=p;if(r->bad_guy)r->bad_guy->proto.destroy(r->bad_guy);Object_destroy(r);}
static void *Room_move(void *p,Direction d){Room *r=p;Room *next=d==NORTH?r->north:d==SOUTH?r->south:d==EAST?r->east:r->west;if(next)next->proto.describe(next);else puts("blocked");return next;}
static int Room_attack(void *p,int damage){Room *r=p;if(!r->bad_guy){puts("empty");return 0;}if(r->bad_guy->proto.attack(r->bad_guy,damage)){r->bad_guy->proto.destroy(r->bad_guy);r->bad_guy=NULL;return 1;}return 0;}
Object RoomProto={.destroy=Room_destroy,.move=Room_move,.attack=Room_attack};
void Map_destroy(void *p){Map *m=p;for(size_t i=0;i<m->count;i++)m->owned[i]->proto.destroy(m->owned[i]);Object_destroy(m);}
void *Map_move(void *p,Direction d){Map *m=p;Room *next=m->location->proto.move(m->location,d);if(next)m->location=next;return next;}
int Map_attack(void *p,int damage){Map *m=p;return m->location->proto.attack(m->location,damage);}
int Map_fill(Map *m,const char *const *names,size_t count){if(count>8)return 0;for(size_t i=0;i<count;i++){Room *r=NEW(Room,(char *)names[i]);if(!r)return 0;m->owned[m->count++]=r;}m->start=m->location=m->owned[0];return 1;}
