// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vlight.h for the primary calling header

#include "Vlight__pch.h"

void Vlight___024root___eval_sample(Vlight___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___eval_sample\n"); );
    Vlight__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vlight___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vlight___024root___eval_ico(Vlight___024root* vlSelf, CData/*0:0*/ firstIteration) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___eval_ico\n"); );
    Vlight__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[1U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VicoTriggered[1U]) 
                                     | (IData)((IData)(firstIteration)));
    {
        // Inlined CFunc: _eval_triggers_vec__ico
        vlSelfRef.__VicoTriggered[0U] = (QData)((IData)(
                                                        ((((IData)(vlSelfRef.reset) 
                                                           != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__reset__0)) 
                                                          << 1U) 
                                                         | ((IData)(vlSelfRef.clock) 
                                                            != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clock__0)))));
        vlSelfRef.__Vtrigprevexpr___TOP__clock__0 = vlSelfRef.clock;
        vlSelfRef.__Vtrigprevexpr___TOP__reset__0 = vlSelfRef.reset;
        if (VL_UNLIKELY(((1U & (~ (IData)(vlSelfRef.__VicoDidInit)))))) {
            vlSelfRef.__VicoDidInit = 1U;
            vlSelfRef.__VicoTriggered[0U] = (1ULL | vlSelfRef.__VicoTriggered[0U]);
            vlSelfRef.__VicoTriggered[0U] = (2ULL | vlSelfRef.__VicoTriggered[0U]);
        }
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vlight___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    return (0U);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vlight___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
void Vlight___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in);

bool Vlight___024root___eval_act(Vlight___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___eval_act\n"); );
    Vlight__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        ((IData)(vlSelfRef.clock) 
                                                         & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clock__1)))));
        vlSelfRef.__Vtrigprevexpr___TOP__clock__1 = vlSelfRef.clock;
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vlight___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vlight___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

bool Vlight___024root___eval_inact(Vlight___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___eval_inact\n"); );
    Vlight__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    return (0U);
}

bool Vlight___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);
void Vlight___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out);

bool Vlight___024root___eval_nba(Vlight___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___eval_nba\n"); );
    Vlight__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vlight___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_body__nba
            if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
                {
                    // Inlined CFunc: _nba_sequent__TOP__0
                    SData/*15:0*/ __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__led;
                    __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__led = 0;
                    IData/*31:0*/ __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__light__DOT__count;
                    __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__light__DOT__count = 0;
                    __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__led 
                        = vlSelfRef.led;
                    __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__light__DOT__count 
                        = vlSelfRef.light__DOT__count;
                    if (vlSelfRef.reset) {
                        __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__led = 1U;
                        __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__light__DOT__count = 0U;
                    } else {
                        if ((0U == vlSelfRef.light__DOT__count)) {
                            __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__led 
                                = ((0x0000fffeU & ((IData)(vlSelfRef.led) 
                                                   << 1U)) 
                                   | (1U & ((IData)(vlSelfRef.led) 
                                            >> 0x0fU)));
                        }
                        __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__light__DOT__count 
                            = ((0x004c4b40U == vlSelfRef.light__DOT__count)
                                ? 0U : ((IData)(1U) 
                                        + vlSelfRef.light__DOT__count));
                    }
                    vlSelfRef.led = __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__led;
                    vlSelfRef.light__DOT__count = __Vinline_0__eval_body__nba___Vinline_0__nba_sequent__TOP__0___Vdly__light__DOT__count;
                }
            }
        }
        Vlight___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

bool Vlight___024root___eval_obs(Vlight___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___eval_obs\n"); );
    Vlight__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    return (0U);
}

bool Vlight___024root___eval_react(Vlight___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___eval_react\n"); );
    Vlight__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    return (0U);
}

void Vlight___024root___eval_postponed(Vlight___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___eval_postponed\n"); );
    Vlight__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

bool Vlight___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___trigger_anySet__ico\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((2U > n));
    return (0U);
}

bool Vlight___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___trigger_anySet__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

void Vlight___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((0U >= n));
}

void Vlight___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

#ifdef VL_DEBUG
void Vlight___024root___eval_debug_assertions(Vlight___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vlight___024root___eval_debug_assertions\n"); );
    Vlight__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clock & 0xfeU)))) {
        Verilated::overWidthError("clock");
    }
    if (VL_UNLIKELY(((vlSelfRef.reset & 0xfeU)))) {
        Verilated::overWidthError("reset");
    }
}
#endif  // VL_DEBUG
