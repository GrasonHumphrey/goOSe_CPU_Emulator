#include <stdbool.h>
#include "reg_8_bit.h"

#ifndef instruction_register_control_h
#define instruction_register_control_h

struct instruction_register_control
{
    // External signals
    bool *clk;
    int *data_bus;
    int *adr_bus;
    bool *reset;
    bool *go;
    bool *eip;
    bool *eip_b;
    bool *ladd;
    bool *ce;
    bool *count;
    bool *lt1;
    bool *lt2;
    bool *lta;
    bool *we;
    bool *lip;
    bool *lip1;
    bool *lip2;
    bool *et;
    bool *et_b;
    bool *lsp1;
    bool *lsp2;
    bool *lspa;
    bool *esp;
    bool *esp_b;
    bool *lrr1;
    bool *lrr2;
    bool *lrra;
    bool *err;
    bool *err_b;
    bool *lbp1;
    bool *lbp2;
    bool *lbpa;
    bool *ebp;
    bool *ebp_b;
    bool *lacc;
    bool *eacc;
    bool *lbuff;
    bool *ebuff;
    int *sel;
    bool *ealu;
    bool *cf;
    bool *zf;
    bool *sf;
    bool *of;
    bool *xf;
    bool *clc;
    bool *linst;
    bool *systemHalt;
    int *ramMem;
    int *charMem;
    int *screenMem;
    int *colorMem;
    int charMemSize;
    int screenMemSize;
    int colorMemSize;
    int charMemLoc;
    int screenMemLoc;
    int colorMemLoc;
    int ramSize;

    // Opcode signals
    bool mema;
    bool memb;
    bool immeda;
    bool immedb;
    bool stora;
    bool storb;
    bool halt;
    bool mov;
    bool add;
    bool sub;
    bool log;
    bool io;
    bool swp;
    bool shl;
    bool shr;
    bool deca;
    bool decb;
    bool inca;
    bool incb;
    bool aux;
    bool jmp;
    bool jz;
    bool jnz;
    bool jm;
    bool jp;
    bool jc;
    bool jnc;
    
    // State variables
    int t;
    bool treset;
    bool ff;
    bool tf;
    //bool execute;
    bool prevclk;
    bool shouldJump;

    int data;
};

typedef struct instruction_register_control Instruction_Register_Control;

void ResetOutputs_IRC(Instruction_Register_Control *irc);
void ResetState_IRC(Instruction_Register_Control *irc);
void ResetOpcodes_IRC(Instruction_Register_Control *irc);
void SetOpcodes_IRC(Instruction_Register_Control *irc);
bool ZeroOperandOpcode_IRC(Instruction_Register_Control *irc);
bool OneOperandOpcode_IRC(Instruction_Register_Control *irc);
void Update_IRC(Instruction_Register_Control *irc, Reg_8_Bit *acc, Reg_8_Bit *buff, int totalCycles);

#endif