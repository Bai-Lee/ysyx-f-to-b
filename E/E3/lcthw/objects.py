from native import *
import shutil
def main():
    original=SRC/'game_original';original.mkdir(exist_ok=True)
    for name,index in [('object.h',1),('object.c',2),('ex19.h',4),('ex19.c',5)]: (original/name).write_text(block(19,index))
    exe,_,_=build('game_original',files=[original/'object.c',original/'ex19.c'])
    o,e,r=execute('game_original',exe,vg=True,expected=(99,),stdin='l\nn\nl\nw\na\n')
    assert 'The great Hall' in o and 'The throne room' in o and 'The arena' in o and 'still alive' in o
    assert re.search(r'definitely lost:\s+[1-9]',e)
    verdict(['LCT-19-BASE'],'PASS_ADAPTED',['game_original'],'Original program truly ran; its graph is never destroyed and Memcheck reports leaks. Derived versions add explicit ownership and cleanup rather than reporting original as memory-clean.')
    d=SRC/'games';d.mkdir(exist_ok=True)
    (d/'object.h').write_text('#include <stddef.h>\n'+block(19,1))
    obj=block(19,2).replace('    *el = proto;','    if(!el) return NULL;\n    *el = proto;').replace('    el->description = strdup(description);','    el->description = strdup(description);\n    if(!el->description){free(el);return NULL;}')
    (d/'object.c').write_text(obj)
    (d/'game.h').write_text('''#ifndef GAME_H
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
''')
    (d/'actors.c').write_text('''#include <stdio.h>
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
''')
    (d/'map_adventure.c').write_text('''#include "game.h"
static int init(void *p){Map *m=p;const char *names[]={"Hall","Throne","Arena","Kitchen","Garden","Tower"};if(!Map_fill(m,names,6))return 0;
Room **r=m->owned;r[0]->north=r[1];r[1]->south=r[0];r[1]->west=r[2];r[2]->east=r[1];r[1]->east=r[3];r[3]->west=r[1];r[3]->north=r[4];r[4]->south=r[3];r[4]->east=r[5];r[5]->west=r[4];
for(int i=0;i<3;i++){int index=(int[]){2,4,5}[i];r[index]->bad_guy=NEW(Monster,"guard");if(!r[index]->bad_guy)return 0;}return 1;}
Object MapProto={.init=init,.destroy=Map_destroy,.move=Map_move,.attack=Map_attack};
''')
    (d/'main_adventure.c').write_text('''#include <stdio.h>
#include <stdlib.h>
#include "game.h"
int main(void){srand(260719);Map *m=NEW(Map,"Adventure");if(!m)return 1;m->location->proto.describe(m->location);int ch;
while((ch=getchar())!=EOF&&ch!='q'){if(ch=='n')m->proto.move(m,NORTH);else if(ch=='s')m->proto.move(m,SOUTH);else if(ch=='e')m->proto.move(m,EAST);else if(ch=='w')m->proto.move(m,WEST);else if(ch=='a')m->proto.attack(m,1+rand()%4);else if(ch=='l')m->location->proto.describe(m->location);}
m->proto.destroy(m);return 0;}
''')
    (d/'map_walk.c').write_text('''#include "game.h"
static int init(void *p){Map *m=p;const char *names[]={"Entry","Bridge","Treasure"};if(!Map_fill(m,names,3))return 0;m->owned[0]->east=m->owned[1];m->owned[1]->west=m->owned[0];m->owned[1]->east=m->owned[2];m->owned[2]->west=m->owned[1];return 1;}
Object MapProto={.init=init,.destroy=Map_destroy,.move=Map_move,.attack=Map_attack};
''')
    (d/'main_walk.c').write_text('''#include <stdio.h>
#include "game.h"
int main(void){Map *m=NEW(Map,"Walk");if(!m)return 1;m->location->proto.describe(m->location);m->proto.move(m,EAST);m->proto.move(m,EAST);puts("treasure reached");m->proto.destroy(m);return 0;}
''')
    tests='''import subprocess
cases=[("",["Hall."]),("w\\\\nq\\\\n",["blocked"]),("n\\\\ne\\\\nn\\\\ne\\\\nq\\\\n",["Throne.","Kitchen.","Garden.","Tower."]),("n\\\\nw\\\\n"+"a\\\\n"*10+"q\\\\n",["Arena.","dead","empty"])]
for data,parts in cases:
 p=subprocess.run(["valgrind","--error-exitcode=99","--leak-check=full","./adventure"],input=data,text=True,capture_output=True);assert p.returncode==0,(p.stdout,p.stderr)
 assert all(x in p.stdout for x in parts);assert "ERROR SUMMARY: 0 errors" in p.stderr and "in use at exit: 0 bytes" in p.stderr
p=subprocess.run(["valgrind","--error-exitcode=99","--leak-check=full","./walk"],text=True,capture_output=True);assert p.returncode==0 and "Entry.\\\\nBridge.\\\\nTreasure.\\\\ntreasure reached" in p.stdout and "ERROR SUMMARY: 0 errors" in p.stderr
print("PASS two games, five scenarios, clean ownership")
'''
    # Generated script contains literal escapes in the C-free Python source.
    (d/'test_games.py').write_text(tests.replace('\\\\n','\\n'))
    (d/'Makefile').write_text('''CC=gcc
CFLAGS=-std=gnu17 -Wall -Werror -g -O0
.PHONY: all clean test
all: adventure walk
adventure: object.o actors.o map_adventure.o main_adventure.o
\t$(CC) $(CFLAGS) $^ -o $@
walk: object.o actors.o map_walk.o main_walk.o
\t$(CC) $(CFLAGS) $^ -o $@
%.o: %.c object.h game.h
\t$(CC) $(CFLAGS) -c $< -o $@
test: all
\tpython3 test_games.py
clean:
\trm -f object.o actors.o map_adventure.o main_adventure.o map_walk.o main_walk.o adventure walk
''')
    # Build on Linux ext4 to retain proper native modes; never change archive sources.
    dest=common.LAB/'games';dest.mkdir(exist_ok=True)
    for p in d.iterdir():shutil.copyfile(p,dest/p.name)
    run('games/build',['make','-j2','all'],cwd=dest,inputs=list(d.glob('*.c'))+[d/'Makefile'])
    o,e,r=run('games/test',['make','test'],cwd=dest,inputs=[d/'test_games.py']);assert 'PASS two games' in o
    run('games/clean',['make','clean'],cwd=dest);assert not (dest/'object.o').exists() and not (dest/'adventure').exists()
    run('games/rebuild',['make','-j2','test'],cwd=dest)
    verdict([f'LCT-19-X{i:02}' for i in range(1,5)],'PASS',['games/build','games/test','games/clean','games/rebuild'],'Expanded to6 rooms/3 monsters; shared object.o/actors.o reused by second Map/main. make test drives five scenarios under Memcheck; make clean includes object.o. Graph owns rooms once; directional edges are borrowed, preventing recursive double-free.')
    print('OBJECT_SYSTEM_DONE',flush=True)
if __name__=='__main__':main()
