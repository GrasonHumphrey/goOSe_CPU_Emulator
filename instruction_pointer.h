#include <stdbool.h>

#ifndef instruction_pointer_h
#define instruction_pointer_h

struct instruction_pointer
{
    bool *count;
    bool *lip;
    bool *lip1;
    bool *lip2;
    bool *clk;
    bool *eip;
    bool *eip_b;
    bool *reset;
    int *adr_bus;
    int *data_bus;

    int adr;
    bool prevclk;
};

typedef struct instruction_pointer Instruction_Pointer;

void Update_Instruction_Pointer(Instruction_Pointer *ip);

#endif