/* Adapted from archived official Icarus usage/vpi.html worked example. */
#include <vpi_user.h>
static PLI_INT32 hello(PLI_BYTE8 *p){(void)p;vpi_printf("Hello, World!\n");return 0;}
static void register_hello(void){s_vpi_systf_data t={0};t.type=vpiSysTask;t.tfname="$hello";t.calltf=hello;vpi_register_systf(&t);}
void (*vlog_startup_routines[])(void)={register_hello,0};
