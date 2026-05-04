#include <stdbool.h>

#ifndef reg_16_bit_h
#define reg_16_bit_h

struct reg_16_bit
{
    bool *lt1;
    bool *lt2;
    bool *lta;
    bool *clk;
    bool *et;
    bool *et_b;
    int *data_bus;
    int *adr_bus;

    int adr;
    bool prevclk;
};

typedef struct reg_16_bit Reg_16_Bit;

void Update_Reg_16_Bit(Reg_16_Bit *reg);

#endif