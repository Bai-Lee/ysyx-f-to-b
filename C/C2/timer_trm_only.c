/* Test-local link support for the official AM test menu. D implements TRM only. */
#include <am.h>
#include <klib.h>
#include <klib-macros.h>
bool cte_init(Context *(*handler)(Event, Context *)) {
  (void)handler;
  panic("D_STAGE_NO_CTE");
  return false;
}
void yield(void) { panic("D_STAGE_NO_CTE"); }
void iset(bool enabled) { (void)enabled; panic("D_STAGE_NO_CTE"); }
