#include <stdbool.h>

#ifndef reg_8_bit_h
#define reg_8_bit_h

struct reg_8_bit
{
    bool *lab;
    bool *eab;
    bool *clk;
    int *data_bus;
    int *alt_out;

    int data;
    bool prevclk;
};

typedef struct reg_8_bit Reg_8_Bit;

void Update_Reg_8_Bit(Reg_8_Bit *reg);

#endif