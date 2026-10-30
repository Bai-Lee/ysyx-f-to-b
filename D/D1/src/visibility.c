int public_add(int x){return x+3;}
static int local_add(int x){return x+3;}
int caller(int x){return public_add(x)+local_add(x);}
