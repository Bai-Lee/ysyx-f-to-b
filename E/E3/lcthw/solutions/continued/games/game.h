#ifndef GAME_H
#define GAME_H
#include "object.h"
typedef struct Monster {Object proto;int hit_points;} Monster;
typedef struct Room {Object proto;Monster *bad_guy;struct Room *north,*south,*east,*west;} Room;
typedef struct Map {Object proto;Room *start,*location;Room *owned[8];size_t count;} Map;
extern Object MonsterProto,RoomProto,MapProto;
void Map_destroy(void *);
void *Map_move(void *,Direction);
int Map_attack(void *,int);
int Map_fill(Map *,const char *const *,size_t);
#endif
