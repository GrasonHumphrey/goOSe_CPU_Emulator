#include <stdbool.h>

#ifndef arithmetic_logic_unit_h
#define arithmetic_logic_unit_h

struct arithmetic_logic_unit
{
    bool *clk;
    int *data_bus;
    int *alu_in_a;
    int *alu_in_b;
    int *sel;
    bool *ealu;
    bool *cf;
    bool *zf;
    bool *sf;
    bool *of;
    bool *xf;
    bool *clc;
    
    int data;
};

typedef struct arithmetic_logic_unit Arithmetic_Logic_Unit;

void Update_ALU(Arithmetic_Logic_Unit *alu);

#endif