// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vlight.h for the primary calling header

#include "Vlight__pch.h"

void Vlight___024root___ctor_var_reset(Vlight___024root* vlSelf);

Vlight___024root::Vlight___024root(Vlight__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vlight___024root___ctor_var_reset(this);
}

void Vlight___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vlight___024root::~Vlight___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
