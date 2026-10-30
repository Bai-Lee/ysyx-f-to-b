/* Test-local links for AM test menu entries outside PA2 TRM/IOE scope. */
#include <am.h>
#include <klib.h>
#include <klib-macros.h>
bool cte_init(Context *(*handler)(Event, Context *)) {
  (void)handler; panic("C2_NO_CTE"); return false;
}
void yield(void) { panic("C2_NO_CTE"); }
void iset(bool enabled) { (void)enabled; panic("C2_NO_CTE"); }
