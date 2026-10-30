// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vlight__pch.h"

//============================================================
// Constructors

Vlight::Vlight(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vlight__Syms(contextp(), _vcname__, this)}
    , m_evalLoop{*this, /*convergeLimit:*/ 10000}
    , clock{vlSymsp->TOP.clock}
    , reset{vlSymsp->TOP.reset}
    , led{vlSymsp->TOP.led}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vlight::Vlight(const char* _vcname__)
    : Vlight(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vlight::~Vlight() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vlight___024root___eval_debug_assertions(Vlight___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD void Vlight___024root___eval_static(Vlight___024root* vlSelf);
VL_ATTR_COLD void Vlight___024root___eval_initial(Vlight___024root* vlSelf);
VL_ATTR_COLD bool Vlight___024root___eval_stl(Vlight___024root* vlSelf, CData/*0:0*/ firstIteration);
void Vlight___024root___eval_sample(Vlight___024root* vlSelf);
bool Vlight___024root___eval_ico(Vlight___024root* vlSelf, CData/*0:0*/ firstIteration);
bool Vlight___024root___eval_act(Vlight___024root* vlSelf);
bool Vlight___024root___eval_inact(Vlight___024root* vlSelf);
bool Vlight___024root___eval_nba(Vlight___024root* vlSelf);
bool Vlight___024root___eval_obs(Vlight___024root* vlSelf);
bool Vlight___024root___eval_react(Vlight___024root* vlSelf);
void Vlight___024root___eval_postponed(Vlight___024root* vlSelf);
VL_ATTR_COLD void Vlight___024root___eval_final(Vlight___024root* vlSelf);
VL_ATTR_COLD void Vlight___024root___eval_dump_triggers__stl(Vlight___024root* vlSelf);
VL_ATTR_COLD void Vlight___024root___eval_dump_triggers__ico(Vlight___024root* vlSelf);
VL_ATTR_COLD void Vlight___024root___eval_dump_triggers__act(Vlight___024root* vlSelf);
VL_ATTR_COLD void Vlight___024root___eval_dump_triggers__nba(Vlight___024root* vlSelf);
VL_ATTR_COLD void Vlight___024root___eval_dump_triggers__obs(Vlight___024root* vlSelf);
VL_ATTR_COLD void Vlight___024root___eval_dump_triggers__react(Vlight___024root* vlSelf);

void Vlight::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vlight::eval_step\n"); );
    m_evalLoop.eval();
}

void Vlight::evalBegin() {
#ifdef VL_DEBUG
    // Debug assertions
    Vlight___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
}

void Vlight::evalEnd() {
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

void Vlight::evalStatic() {
    Vlight___024root___eval_static(&(vlSymsp->TOP));
}

void Vlight::evalInitial() {
    Vlight___024root___eval_initial(&(vlSymsp->TOP));
}

bool Vlight::evalStl(bool firstIteration) {
    return Vlight___024root___eval_stl(&(vlSymsp->TOP), firstIteration);
}

void Vlight::evalSample() {
    Vlight___024root___eval_sample(&(vlSymsp->TOP));
}

bool Vlight::evalIco(bool firstIteration) {
    return Vlight___024root___eval_ico(&(vlSymsp->TOP), firstIteration);
}

bool Vlight::evalAct() {
    return Vlight___024root___eval_act(&(vlSymsp->TOP));
}

bool Vlight::evalInact() {
    return Vlight___024root___eval_inact(&(vlSymsp->TOP));
}

bool Vlight::evalNba() {
    return Vlight___024root___eval_nba(&(vlSymsp->TOP));
}

bool Vlight::evalObs() {
    return Vlight___024root___eval_obs(&(vlSymsp->TOP));
}

bool Vlight::evalReact() {
    return Vlight___024root___eval_react(&(vlSymsp->TOP));
}

void Vlight::evalPostponed() {
    Vlight___024root___eval_postponed(&(vlSymsp->TOP));
}

void Vlight::evalFinal() {
    Vlight___024root___eval_final(&(vlSymsp->TOP));
}

VL_ATTR_COLD void Vlight::dumpTriggersStl() {
    Vlight___024root___eval_dump_triggers__stl(&(vlSymsp->TOP));
}

VL_ATTR_COLD void Vlight::dumpTriggersIco() {
    Vlight___024root___eval_dump_triggers__ico(&(vlSymsp->TOP));
}

VL_ATTR_COLD void Vlight::dumpTriggersAct() {
    Vlight___024root___eval_dump_triggers__act(&(vlSymsp->TOP));
}

VL_ATTR_COLD void Vlight::dumpTriggersNba() {
    Vlight___024root___eval_dump_triggers__nba(&(vlSymsp->TOP));
}

VL_ATTR_COLD void Vlight::dumpTriggersObs() {
    Vlight___024root___eval_dump_triggers__obs(&(vlSymsp->TOP));
}

VL_ATTR_COLD void Vlight::dumpTriggersReact() {
    Vlight___024root___eval_dump_triggers__react(&(vlSymsp->TOP));
}

//============================================================
// Events and timing
bool Vlight::eventsPending() { return false; }

uint64_t Vlight::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vlight::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

VL_ATTR_COLD void Vlight::final() {
    contextp()->executingFinal(true);
    evalFinal();
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vlight::hierName() const { return vlSymsp->name(); }
const char* Vlight::modelName() const { return "Vlight"; }
unsigned Vlight::threads() const { return 1; }
void Vlight::prepareClone() const { contextp()->prepareClone(); }
void Vlight::atClone() const {
    contextp()->threadPoolpOnClone();
}
