#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "instruction_pointer.h"
#include "address_buffer.h"
#include "reg_8_bit.h"
#include "reg_16_bit.h"
#include "arithmetic_logic_unit.h"
#include "instruction_register_control.h"
#include "CPU.h"

Instruction_Pointer ip;
Address_Buffer ab;
Reg_16_Bit tr;
Reg_16_Bit rr;
Reg_16_Bit sp;
Reg_16_Bit bp;
Arithmetic_Logic_Unit alu;
Reg_8_Bit acc;
Reg_8_Bit buff;
Instruction_Register_Control irc;

#define CHAR_MEM_SIZE 0x1000
#define SCREEN_MEM_SIZE 0x2000
#define COLOR_MEM_SIZE 0x408
#define STACK_PTR_START 0xDFF
#define KEY_BUF_BASE 0xDE0
#define KEY_BUF_PTR_LOC 0x0004

#define CODE_START_LOC 0x100
#define CHAR_MEM_LOC 0x1000
#define SCREEN_MEM_LOC 0x2000
#define COLOR_MEM_LOC 0x4000

#define RAM_SIZE 0x8000


bool clk;
int totalCycles;

// Declare memory
int ramMem[RAM_SIZE];
int charMem[CHAR_MEM_SIZE];
int screenMem[SCREEN_MEM_SIZE];
int colorMem[COLOR_MEM_SIZE];

int main()
{
    clk = false;
    // Define wire pointers
    bool count = false;
    bool lip = false;
    bool lip1 = false;
    bool lip2 = false;
    bool eip = false;
    bool eip_b = false;
    bool reset = false;
    int adr_bus = 0;
    bool ladd = false;
    bool we = false;
    bool ce = false;
    int data_bus = 0;

    bool linst = false;
    bool go = false;

    bool lt1 = false;
    bool lt2 = false;
    bool lta = false;
    bool et = false;
    bool et_b = false;

    bool lsp1 = false;
    bool lsp2 = false;
    bool lspa = false;
    bool esp = false;
    bool esp_b = false;

    bool lbp1 = false;
    bool lbp2 = false;
    bool lbpa = false;
    bool ebp = false;
    bool ebp_b = false;

    bool lrr1 = false;
    bool lrr2 = false;
    bool lrra = false;
    bool err = false;
    bool err_b = false;

    bool lacc = false;
    bool eacc = false;
    bool lbuff = false;
    bool ebuff = false;
    int acc_alu_out = 0;
    int buff_alu_out = 0;

    int alu_sel = 0;
    bool cf = false;
    bool zf = false;
    bool sf = false;
    bool of = false;
    bool xf = false;
    bool clc = false;
    bool ealu = false;


    totalCycles = 0;
    bool systemHalt = false;


    // Define components
    // Instruction Pointer
    ip.count = &count;
    ip.lip = &lip;
    ip.lip1 = &lip1;
    ip.lip2 = &lip2;
    ip.clk = &clk;
    ip.eip = &eip;
    ip.eip_b = &eip_b;
    ip.reset = &reset;
    ip.adr_bus = &adr_bus;
    ip.data_bus = &data_bus;
    ip.prevclk = false;
    ip.adr = CODE_START_LOC;

    // Address Buffer
    ab.ladd = &ladd;
    ab.clk = &clk;
    ab.we = &we;
    ab.ce = &ce;
    ab.adr_bus = &adr_bus;
    ab.data_bus = &data_bus;
    ab.reset = &reset;
    ab.prevclk = false;
    ab.memory = ramMem;

    // Temporary Register
    tr.lt1 = &lt1;
    tr.lt2 = &lt2;
    tr.lta = &lta;
    tr.clk = &clk;
    tr.et = &et;
    tr.et_b = &et_b;
    tr.data_bus = &data_bus;
    tr.adr_bus = &adr_bus;
    tr.prevclk = false;

    // Restore Register
    rr.lt1 = &lrr1;
    rr.lt2 = &lrr2;
    rr.lta = &lrra;
    rr.clk = &clk;
    rr.et = &err;
    rr.et_b = &err_b;
    rr.data_bus = &data_bus;
    rr.adr_bus = &adr_bus;
    rr.prevclk = false;

    // Stack Pointer Register
    sp.lt1 = &lsp1;
    sp.lt2 = &lsp2;
    sp.lta = &lspa;
    sp.clk = &clk;
    sp.et = &esp;
    sp.et_b = &esp_b;
    sp.data_bus = &data_bus;
    sp.adr_bus = &adr_bus;
    sp.prevclk = false;
    sp.adr = STACK_PTR_START;

    // Base Pointer Register
    bp.lt1 = &lbp1;
    bp.lt2 = &lbp2;
    bp.lta = &lbpa;
    bp.clk = &clk;
    bp.et = &ebp;
    bp.et_b = &ebp_b;
    bp.data_bus = &data_bus;
    bp.adr_bus = &adr_bus;
    bp.prevclk = false;
    bp.adr = STACK_PTR_START;

    // ALU
    alu.clk = &clk;
    alu.data_bus = &data_bus;
    alu.alu_in_a = &acc_alu_out;
    alu.alu_in_b = &buff_alu_out;
    alu.sel = &alu_sel;
    alu.ealu = &ealu;
    alu.cf = &cf;
    alu.zf = &zf;
    alu.sf = &sf;
    alu.of = &of;
    alu.xf = &xf;
    alu.clc = &clc;

    // Accumulator Register
    acc.lab = &lacc;
    acc.eab = &eacc;
    acc.clk = &clk;
    acc.data_bus = &data_bus;
    acc.alt_out = &acc_alu_out;
    acc.prevclk = false;

    // Buffer Register
    buff.lab = &lbuff;
    buff.eab = &ebuff;
    buff.clk = &clk;
    buff.data_bus = &data_bus;
    buff.alt_out = &buff_alu_out;
    buff.prevclk = false;

    // Instruction Register Controller
    irc.clk = &clk;
    irc.data_bus = &data_bus;
    irc.adr_bus = &adr_bus;
    irc.reset = &reset;
    irc.go = &go;
    irc.eip = &eip;
    irc.eip_b = &eip_b;
    irc.ladd = &ladd;
    irc.ce = &ce;
    irc.count = &count;
    irc.lt1 = &lt1;
    irc.lt2 = &lt2;
    irc.lta = &lta;
    irc.we = &we;
    irc.lip = &lip;
    irc.lip1 = &lip1;
    irc.lip2 = &lip2;
    irc.et = &et;
    irc.et_b = &et_b;
    irc.lsp1 = &lsp1;
    irc.lsp2 = &lsp2;
    irc.lspa = &lspa;
    irc.esp = &esp;
    irc.esp_b = &esp_b;
    irc.lrr1 = &lrr1;
    irc.lrr2 = &lrr2;
    irc.lrra = &lrra;
    irc.err = &err;
    irc.err_b = &err_b;
    irc.lbp1 = &lbp1;
    irc.lbp2 = &lbp2;
    irc.lbpa = &lbpa;
    irc.ebp = &ebp;
    irc.ebp_b = &ebp_b;
    irc.lacc = &lacc;
    irc.eacc = &eacc;
    irc.lbuff = &lbuff;
    irc.ebuff = &ebuff;
    irc.sel = &alu_sel;
    irc.ealu = &ealu;
    irc.cf = &cf;
    irc.zf = &zf;
    irc.sf = &sf;
    irc.of = &of;
    irc.xf = &xf;
    irc.clc = &clc;
    irc.linst = &linst;
    irc.systemHalt = &systemHalt;
    irc.ramMem = ramMem;
    irc.charMem = charMem;
    irc.screenMem = screenMem;
    irc.colorMem = colorMem;
    irc.ramSize = RAM_SIZE;
    irc.charMemSize = CHAR_MEM_SIZE;
    irc.charMemLoc = CHAR_MEM_LOC;
    irc.screenMemSize = SCREEN_MEM_SIZE;
    irc.screenMemLoc = SCREEN_MEM_LOC;
    irc.colorMemSize = COLOR_MEM_SIZE;
    irc.colorMemLoc = COLOR_MEM_LOC;
    irc.data = 0;
    irc.mema = false;
    irc.memb = false;
    irc.immeda = false;
    irc.immedb = false;
    irc.stora = false;
    irc.storb = false;
    irc.halt = false;
    irc.mov = false;
    irc.add = false;
    irc.sub = false;
    irc.log = false;
    irc.io = false;
    irc.swp = false;
    irc.shl = false;
    irc.shr = false;
    irc.deca = false;
    irc.decb = false;
    irc.inca = false;
    irc.incb = false;
    irc.aux = false;
    irc.jmp = false;
    irc.jz = false;
    irc.jnz = false;
    irc.jm = false;
    irc.jp = false;
    irc.jc = false;
    irc.jnc = false;
    irc.t = -1;
    irc.treset = false;
    irc.ff = false;
    irc.tf = false;
    //irc.execute = false;
    irc.shouldJump = false;
    irc.prevclk = false;
 
    Load_Memory_From_File(&ab);
    
    while (!systemHalt)
    {
        Toggle_CLK();
        totalCycles += 1;
        //printf("Toggle CLK\n");
    }
}

void Update_All()
{
    Update_ALU(&alu);
    Update_Instruction_Pointer(&ip);
    Update_Address_Buffer(&ab);
    Update_Reg_16_Bit(&tr);
    Update_Reg_8_Bit(&acc);
    Update_Reg_8_Bit(&buff);
    Update_Reg_16_Bit(&sp);
    Update_Reg_16_Bit(&bp);
    Update_Reg_16_Bit(&rr);
    Update_IRC(&irc, &acc, &buff, totalCycles);
}

void Toggle_CLK()
{
    clk = false;
    Update_All();
    clk = true;
    Update_All();
    clk = false;
}