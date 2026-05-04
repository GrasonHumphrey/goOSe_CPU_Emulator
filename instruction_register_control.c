#include "instruction_register_control.h"
#include "reg_8_bit.h"

void ResetOutputs_IRC(Instruction_Register_Control *irc)
{
    *(irc->eip) = false;
    *(irc->eip_b) = false;
    *(irc->ladd) = false;
    *(irc->ce) = false;
    *(irc->lt1) = false;
    *(irc->lt2) = false;
    *(irc->lta) = false;
    *(irc->we) = false;
    *(irc->count) = false;
    *(irc->lip) = false;
    *(irc->lip1) = false;
    *(irc->lip2) = false;
    *(irc->et) = false;
    *(irc->et_b) = false;
    *(irc->lacc) = false;
    *(irc->eacc) = false;
    *(irc->lbuff) = false;
    *(irc->ebuff) = false;
    *(irc->sel) = 0;
    *(irc->ealu) = false;
    *(irc->lrr1) = false;
    *(irc->lrr2) = false;
    *(irc->lrra) = false;
    *(irc->err) = false;
    *(irc->err_b) = false;
    *(irc->lsp1) = false;
    *(irc->lsp2) = false;
    *(irc->lspa) = false;
    *(irc->esp) = false;
    *(irc->esp_b) = false;
    *(irc->lbp1) = false;
    *(irc->lbp2) = false;
    *(irc->lbpa) = false;
    *(irc->ebp) = false;
    *(irc->ebp_b) = false;
    *(irc->clc) = false;
    //*(irc->data) = 0
}

void ResetState_IRC(Instruction_Register_Control *irc)
{
    irc->t = -1;
    irc->treset = false;
    irc->ff = false;
    irc->tf = false;
    *(irc->linst) = false;
    irc->shouldJump = false;
    //*(irc->execute) = false;
}

void ResetOpcodes_IRC(Instruction_Register_Control *irc)
{
    irc->mema = false;
    irc->memb = false;
    irc->immeda = false;
    irc->immedb = false;
    irc->stora = false;
    irc->storb = false;
    irc->halt = false;
    irc->mov = false;
    irc->add = false;
    irc->sub = false;
    irc->log = false;
    irc->io = false;
    irc->swp = false;
    irc->shl = false;
    irc->shr = false;
    irc->inca = false;
    irc->incb = false;
    irc->aux = false;
    irc->deca = false;
    irc->decb = false;
    irc->jmp = false;
    irc->jz = false;
    irc->jnz = false;
    irc->jm = false;
    irc->jp = false;
    irc->jc = false;
    irc->jnc = false;
}

void SetOpcodes_IRC(Instruction_Register_Control *irc)
{
    int lower = irc->data & 0x0F;
    int upper = (irc->data & 0xF0) >> 4;

    if (lower == 0x1)
    {
        irc->mema = true;
    }
    else if (lower == 0x2)
    {
        irc->memb = true;
    }
    else if (lower == 0x3)
    {
        irc->immeda = true;
    }
    else if (lower == 0x4)
    {
        irc->immedb = true;
    }
    else if (lower == 0x5)
    {
        irc->stora = true;
    }
    else if (lower == 0x6)
    {
        irc->storb = true;
    }
    else if (lower == 0x7)
    {
        irc->swp = true;
    }
    else if (lower == 0x8)
    {
        irc->shl = true;
    }
    else if (lower == 0x9)
    {
        irc->shr = true;
    }
    else if (lower == 0xA)
    {
        irc->deca = true;
    }
    else if (lower == 0xB)
    {
        irc->decb = true;
    }
    else if (lower == 0xC)
    {
        irc->inca = true;
    }
    else if (lower == 0xD)
    {
        irc->incb = true;
    }
    else if (lower == 0xE)
    {
        irc->aux = true;
    }
    else if (lower == 0xF)
    {
        irc->halt = true;
        *(irc->systemHalt) = true;
        printf("HALT received, exiting...");
    }

    if (upper == 0x0)
    {
        irc->mov = true;
    }
    else if (upper == 0x1)
    {
        irc->add = true;
    }
    else if (upper == 0x2)
    {
        irc->log = true;
    }
    else if (upper == 0x3)
    {
        irc->io = true;
    }
    else if (upper == 0x4)
    {
        irc->sub = true;
    }
    else if (upper == 0x8)
    {
        irc->jmp = true;
    }
    else if (upper == 0x9)
    {
        irc->jz = true;
    }
    else if (upper == 0xA)
    {
        irc->jnz = true;
    }
    else if (upper == 0xB)
    {
        irc->jm = true;
    }
    else if (upper == 0xC)
    {
        irc->jp = true;
    }
    else if (upper == 0xD)
    {
        irc->jc = true;
    }
    else if (upper == 0xE)
    {
        irc->jnc = true;
    }
    else if (upper == 0xF)
    {
        irc->halt = true;
        *(irc->systemHalt) = true;
        // printf("exiting...")
    }
}

bool ZeroOperandOpcode_IRC(Instruction_Register_Control *irc)
{
    return (irc->io ||
            (irc->add && irc->immedb) ||
            (irc->sub && irc->immedb) ||
            (irc->log && irc->inca) ||
            (irc->log && irc->incb) ||
            (irc->deca && irc->log) ||
            (irc->decb && irc->log) ||
            (irc->log && irc->deca) ||
            (irc->mov && irc->swp) ||
            irc->halt ||
            (irc->log && irc->shl) ||
            (irc->log && irc->shr) ||
            (irc->log && irc->mema) ||
            (irc->log && irc->memb) ||
            (irc->log && irc->immeda) ||
            (irc->log && irc->immedb) ||
            (irc->io && irc->mema) ||
            (irc->io && irc->memb) ||
            (irc->jmp && irc->deca) ||
            (irc->jmp && irc->aux) ||
            (irc->add && irc->stora) ||
            (irc->jmp && irc->decb) ||
            (irc->mov && irc->inca) ||
            (irc->jmp && irc->inca) ||
            (irc->jmp && irc->immedb) ||
            (irc->jz && irc->immedb) ||  // Jump to offset if zero
            (irc->jnz && irc->immedb) || // Jump to offset if non-zero
            (irc->jm && irc->immedb) ||  // Jump to offset if negative
            (irc->jp && irc->immedb) ||  // Jump to offset if positive
            (irc->jc && irc->immedb) ||  // Jump to offset if carry occurred
            (irc->jnc && irc->immedb) || // Jump to offset if carry did not occur
            (irc->jc && irc->shl) ||     // Jump to offset if carry occurred
            (irc->jnc && irc->shl) ||
            (irc->jmp && irc->storb) ||
            (irc->jz && irc->storb) ||
            (irc->jnz && irc->storb) ||
            (irc->jm && irc->storb) ||
            (irc->jp && irc->storb) ||
            (irc->jc && irc->storb) ||
            (irc->jnc && irc->storb) ||
            (irc->jc && irc->deca) ||
            (irc->jnc && irc->deca) ||
            (irc->jz && irc->aux) ||
            (irc->jnz && irc->aux));
}

bool OneOperandOpcode_IRC(Instruction_Register_Control *irc)
{
    return ((irc->mov && irc->immeda) || // Immediate move into A
            (irc->mov && irc->immedb) || // Immediate move into B
            (irc->mov && irc->deca) ||
            (irc->mov && irc->decb) ||
            (irc->add && irc->immeda) || // Immediately add
            (irc->sub && irc->immeda) || // Immediately subtract
            (irc->log && irc->shr) ||
            (irc->log && irc->shl) || // Left && right bit shift
            (irc->jmp && irc->immeda) ||
            (irc->jz && irc->immeda) ||  // Jump to offset if zero
            (irc->jnz && irc->immeda) || // Jump to offset if non-zero
            (irc->jm && irc->immeda) ||  // Jump to offset if negative
            (irc->jp && irc->immeda) ||  // Jump to offset if positive
            (irc->jc && irc->immeda) ||  // Jump to offset if carry occurred
            (irc->jnc && irc->immeda) || // Jump to offset if carry did not occur
            (irc->jc && irc->swp) ||     // Jump to offset if overflow occurred
            (irc->jnc && irc->swp) ||    // Jump to offset if overflow did not occur
            (irc->jmp && irc->stora) ||
            (irc->jz && irc->stora) ||
            (irc->jnz && irc->stora) ||
            (irc->jm && irc->stora) ||
            (irc->jp && irc->stora) ||
            (irc->jc && irc->stora) ||
            (irc->jnc && irc->stora) ||
            (irc->jc && irc->shr) ||
            (irc->jnc && irc->shr) ||
            (irc->log && irc->stora) ||
            (irc->log && irc->storb) ||
            (irc->log && irc->swp) ||
            (irc->jmp && irc->shl) ||
            (irc->jmp && irc->shr) ||
            (irc->jmp && irc->swp) ||
            (irc->jnz && irc->incb));
}

void Update_IRC(Instruction_Register_Control *irc, Reg_8_Bit *acc, Reg_8_Bit *buff, int totalCycles)
{
    // always @ posedge clk
    if ((!irc->prevclk) && *(irc->clk))
    {
        ResetOutputs_IRC(irc);
        irc->t += 1;
        if (*(irc->linst))
        {
            // Load new instruction
            ResetOpcodes_IRC(irc);
            irc->data = *(irc->data_bus);
            //printf("IRC data: %02X\n", irc->data);
            SetOpcodes_IRC(irc);
        }
        if (*(irc->reset) || irc->treset || irc->halt)
        {
            // Reset IRC
            // printf("IRC reset")
            ResetOutputs_IRC(irc);
            ResetOpcodes_IRC(irc);
            ResetState_IRC(irc);
        }
        // Opcode Fetch
        if (irc->ff == 0 && irc->tf == 0)
        {
            //printf ("op fetch");
            if (irc->t == 0)
            {
                ResetOutputs_IRC(irc);
                *(irc->eip) = true;
                *(irc->ladd) = true;
                //printf("****ladd****\n");
            }
            else if (irc->t == 1)
            {
                *(irc->ce) = true;
                *(irc->linst) = true;
                //printf("****linst****\n");
            }
            else if (irc->t == 2)
            {
                *(irc->linst) = false;
                *(irc->count) = true;
                //printf("Opcode: %02X\n", *(irc->data_bus));
                if (ZeroOperandOpcode_IRC(irc))
                {
                    // Opcode with no operand, continue to execute
                    irc->tf = true;
                    // printf("Zero operand opcode")
                }
                else
                {
                    // Fetch first operand for opcodes with 1 || more operands
                    irc->t = -1;
                    irc->ff = true;
                    // printf("More than zero operand opcode")
                }
            }
            // First Operand Fetch
        }
        else if (irc->ff)
        {
            // printf ("ff fetch")
            if (irc->t == 0)
            {
                ResetOutputs_IRC(irc);
                *(irc->eip) = true;
                *(irc->ladd) = true;
            }
            else if (irc->t == 1)
            {
                *(irc->ce) = true;
                *(irc->lt1) = true;
            }
            else if (irc->t == 2)
            {
                *(irc->count) = true;
                irc->tf = true;
                irc->ff = false;
                if (!OneOperandOpcode_IRC(irc))
                {
                    irc->t = -1;
                }
            }
            // Second Operand Fetch
        }
        else if (irc->tf)
        {
            // printf ("tf fetch")
            // printf("t) { " + str(irc->t))
            if (irc->t == 0)
            {
                ResetOutputs_IRC(irc);
                *(irc->eip) = true;
                *(irc->ladd) = true;
            }
            else if (irc->t == 1)
            {
                *(irc->ce) = true;
                *(irc->lt2) = true;
            }
            else if (irc->t == 2)
            {
                *(irc->count) = true;
            }
            else if (irc->t >= 3)
            {
                // Execute

                // MOV into A Immediate operation
                if (irc->mov && irc->immeda)
                {
                    // printf ("mov")
                    if (irc->t == 3)
                    {
                        *(irc->et) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        irc->treset = true;
                    }
                    // MOV into B Immediate operation
                }
                else if (irc->mov && irc->immedb)
                {
                    if (irc->t == 3)
                    {
                        *(irc->et) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // printf("CF after MOV into B) { " + str(*(irc->cf)))
                        irc->treset = true;
                    }
                    // MOV A into MEM
                }
                else if (irc->mov && irc->stora)
                {
                    if (irc->t == 3)
                    {
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                        // printf("here")
                    }
                    else if (irc->t == 4)
                    {
                        *(irc->eacc) = true;
                        *(irc->we) = true;
                    }
                    else if (irc->t == 5)
                    {
                        irc->treset = true;
                    }
                    // MOV B into MEM
                }
                else if (irc->mov && irc->storb)
                {
                    if (irc->t == 3)
                    {
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 4)
                    {
                        *(irc->ebuff) = true;
                        // printf("Enable B")
                        // printf("Count) { " + str(*(irc->count)))
                        *(irc->we) = true;
                    }
                    else if (irc->t == 5)
                    {
                        irc->treset = true;
                    }
                    // MOV MEM into A
                }
                else if (irc->mov && irc->mema)
                {
                    // printf("MOV MEM into A")
                    if (irc->t == 3)
                    {
                        // printf("Set LADD")
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // printf("Clear LADD")
                        *(irc->ce) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 5)
                    {
                        irc->treset = true;
                        // global totalCycles
                        // printf("Finish MOV MEM into A")
                    }
                    // MOV MEM into B
                }
                else if (irc->mov && irc->memb)
                {
                    if (irc->t == 3)
                    {
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 4)
                    {
                        *(irc->ce) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        irc->treset = true;
                    }
                    // STO) { Store A into offset at B from given address in MEM
                }
                else if (irc->mov && irc->shr)
                {
                    if (irc->t == 3)
                    {
                        // Save A
                        *(irc->lrr1) = true;
                        *(irc->eacc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Load lower byte of address into A
                        *(irc->et) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Add A && B
                        *(irc->lacc) = true;
                        *(irc->ealu) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 6)
                    {
                        // Move result to temp1
                        // printf("A+B) { " + hex(*(irc->data_bus)))
                        *(irc->eacc) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Load high byte of address into A
                        *(irc->lacc) = true;
                        *(irc->et_b) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Decide if ( upper byte of BP needs to be incremented
                        // printf("BP_B) { " + hex(*(irc->data_bus)))
                        if (*(irc->xf))
                        {
                            *(irc->lacc) = true;
                            *(irc->ealu) = true;
                            if (*(irc->sf))
                            {
                                // Offset was negative, decrement A
                                *(irc->sel) = 5;
                            }
                            else
                            {
                                // Offset was positive, increment A
                                *(irc->sel) = 4;
                            }
                        }
                    }
                    else if (irc->t == 9)
                    {
                        // Move result to temp2
                        *(irc->eacc) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Move temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Write saved value of A && restore A
                        // printf("Address) { " + hex(*(irc->adr_bus)))
                        *(irc->err) = true;
                        *(irc->we) = true;
                        *(irc->lacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Call finished
                        irc->treset = true;
                        // printf("finish STO")
                    }
                    // LDO) { Load into A from offset at B from given address in MEM
                }
                else if (irc->mov && irc->shl)
                {
                    if (irc->t == 3)
                    {
                        // Load lower byte of address into A
                        *(irc->et) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Add A && B
                        *(irc->lacc) = true;
                        *(irc->ealu) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 5)
                    {
                        // Move result to temp1
                        // printf("A+B) { " + hex(*(irc->data_bus)))
                        *(irc->eacc) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Load high byte of address into A
                        *(irc->lacc) = true;
                        *(irc->et_b) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Decide if ( upper byte of BP needs to be incremented
                        // printf("BP_B) { " + hex(*(irc->data_bus)))
                        if (*(irc->xf))
                        {
                            *(irc->lacc) = true;
                            *(irc->ealu) = true;
                            if (*(irc->sf))
                            {
                                // Offset was negative, decrement A
                                *(irc->sel) = 5;
                            }
                            else
                            {
                                // Offset was positive, increment A
                                *(irc->sel) = 4;
                            }
                        }
                    }
                    else if (irc->t == 8)
                    {
                        // Move result to temp2
                        *(irc->eacc) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Move temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Read into A from MEM
                        // printf("Address) { " + hex(*(irc->adr_bus)))
                        *(irc->ce) = true;
                        *(irc->lacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Call finished
                        irc->treset = true;
                        // printf("finish poke")
                    }
                    // STZ <immed>) { Store A into offset at B from given zero-page pointer address
                }
                else if (irc->mov && irc->decb)
                {
                    if (irc->t == 3)
                    {
                        // Save A to RR1
                        *(irc->eacc) = true;
                        *(irc->lrr1) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Load 0 into T2
                        *(irc->lt2) = true;
                        *(irc->data_bus) = 0x0;
                    }
                    else if (irc->t == 5)
                    {
                        // Load temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Read from MEM into A
                        *(irc->ce) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Add offset in B to A, then save to RR2
                        *(irc->ealu) = true;
                        *(irc->lrr2) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 8)
                    {
                        // Load lower byte of address to A from T1
                        *(irc->et) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Increment lower byte of address
                        *(irc->ealu) = true;
                        *(irc->lt1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 10)
                    {
                        // Load incremented temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Read from MEM into T2
                        *(irc->ce) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Move saved address in RR2 to T1
                        *(irc->err_b) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Load address in temp reg to address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Write stored A in RR1 to MEM && restore A
                        *(irc->err) = true;
                        *(irc->we) = true;
                        *(irc->clc) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 15)
                    {
                        // Finish STZ
                        irc->treset = true;
                    }
                    // LDZ <immed>) { Load A from offset at B from given zero-page pointer address
                }
                else if (irc->mov && irc->deca)
                {
                    if (irc->t == 3)
                    {
                        // Load 0 into T2
                        *(irc->clc) = true;
                        *(irc->lt2) = true;
                        *(irc->data_bus) = 0x0;
                    }
                    else if (irc->t == 4)
                    {
                        // Load temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Read from MEM into A
                        *(irc->ce) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Add offset in B to A, then save to RR2
                        *(irc->ealu) = true;
                        *(irc->lrr2) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 7)
                    {
                        // Load lower byte of address to A from T1
                        *(irc->et) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Increment lower byte of address
                        *(irc->ealu) = true;
                        *(irc->lt1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 9)
                    {
                        // Load incremented temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Read from MEM into T2
                        *(irc->ce) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Move saved address in RR2 to T1
                        *(irc->err_b) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Load address in temp reg to address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Read MEM into A
                        *(irc->lacc) = true;
                        *(irc->ce) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Finish LDZ
                        irc->treset = true;
                    }
                    // LDZ Ar) { Load A from offset at B from Ar zero-page pointer address
                }
                else if (irc->mov && irc->inca)
                {
                    if (irc->t == 3)
                    {
                        // Load 0 into T2
                        *(irc->clc) = true;
                        *(irc->lt2) = true;
                        *(irc->data_bus) = 0x0;
                    }
                    else if (irc->t == 4)
                    {
                        // Load Ar into T1
                        *(irc->eacc) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Read from MEM into A
                        *(irc->ce) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Add offset in B to A, then save to RR2
                        *(irc->ealu) = true;
                        *(irc->lrr2) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 8)
                    {
                        // Load lower byte of address to A from T1
                        *(irc->et) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Increment lower byte of address
                        *(irc->ealu) = true;
                        *(irc->lt1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 10)
                    {
                        // Load incremented temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Read from MEM into T2
                        *(irc->ce) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Move saved address in RR2 to T1
                        *(irc->err_b) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Load address in temp reg to address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Read MEM into A
                        // printf("LDZ from address) { " + hex(*(irc->adr_bus)))
                        *(irc->lacc) = true;
                        *(irc->ce) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 15)
                    {
                        // Finish LDZ
                        irc->treset = true;
                    }
                    // ADD Immediate
                }
                else if (irc->add && irc->immeda)
                {
                    if (irc->t == 3)
                    {
                        // Save B reg
                        *(irc->ebuff) = true;
                        *(irc->lrr1) = true;
                    }
                    else if (irc->t == 4)
                    {
                        *(irc->et) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 6)
                    {
                        // Restore B reg
                        *(irc->lbuff) = true;
                        *(irc->err) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 7)
                    {
                        irc->treset = true;
                        // printf("Finish ADD Immediate")
                    }

                    // ADD MEM
                }
                else if (irc->add && irc->mema)
                {
                    if (irc->t == 3)
                    {
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 4)
                    {
                        *(irc->ce) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        irc->treset = true;
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->sel) = 0;
                    }

                    // ADD B to A
                }
                else if (irc->add && irc->immedb)
                {
                    if (irc->t == 3)
                    {
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        // printf("Add t=3")
                        *(irc->sel) = 0;
                        // printf(*(irc->data_bus))
                    }
                    else if (irc->t == 4)
                    {
                        irc->treset = true;
                    }
                    // Clear carry flag
                }
                else if (irc->add && irc->stora)
                {
                    if (irc->t == 3)
                    {
                        *(irc->clc) = true;
                        // printf(*(irc->data_bus))
                    }
                    else if (irc->t == 4)
                    {
                        irc->treset = true;
                    }
                    // SUB Immediate
                }
                else if (irc->sub && irc->immeda)
                {
                    if (irc->t == 3)
                    {
                        // Save B reg
                        *(irc->ebuff) = true;
                        *(irc->lrr1) = true;
                    }
                    else if (irc->t == 4)
                    {
                        *(irc->et) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->sel) = 1;
                    }
                    else if (irc->t == 6)
                    {
                        // Restore B reg
                        *(irc->lbuff) = true;
                        *(irc->err) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 7)
                    {
                        irc->treset = true;
                        // printf("Finish SUB immediate")
                    }
                    // SUB MEM
                }
                else if (irc->sub && irc->mema)
                {
                    // printf("sub mem")
                    if (irc->t == 3)
                    {
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 4)
                    {
                        *(irc->ce) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        irc->treset = true;
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->sel) = 1;
                    }

                    // SUB B from A
                }
                else if (irc->sub && irc->immedb)
                {
                    // printf("Sub A-B")
                    if (irc->t == 3)
                    {
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->sel) = 1;
                    }
                    else if (irc->t == 4)
                    {
                        // printf("CF after sub) { " + str(*(irc->cf)))
                        irc->treset = true;
                    }

                    // Swap A && B
                }
                else if (irc->swp && irc->mov)
                {
                    if (irc->t == 3)
                    {
                        // printf("Start SWP")
                        *(irc->eacc) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 4)
                    {
                        *(irc->ebuff) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 5)
                    {
                        *(irc->lbuff) = true;
                        *(irc->et) = true;
                    }
                    else if (irc->t == 6)
                    {
                        irc->treset = true;
                        // printf("Finish swap")
                    }
                    // Jump to memory address
                }
                else if (((irc->jmp && irc->mema) ||
                          (irc->jz && irc->mema) ||
                          (irc->jnz && irc->mema) ||
                          (irc->jm && irc->mema) ||
                          (irc->jp && irc->mema) ||
                          (irc->jc && irc->mema) ||
                          (irc->jnc && irc->mema) ||
                          (irc->jc && irc->memb) ||
                          (irc->jnc && irc->memb)))
                {
                    if (irc->t == 3)
                    {
                        if (((irc->jmp && irc->mema) ||
                             (irc->jz && irc->mema && *(irc->zf)) ||
                             (irc->jnz && irc->mema && !*(irc->zf)) ||
                             (irc->jm && irc->mema && *(irc->sf)) ||
                             (irc->jp && irc->mema && !*(irc->sf)) ||
                             (irc->jc && irc->mema && *(irc->cf)) ||
                             (irc->jnc && irc->mema && !*(irc->cf)) ||
                             (irc->jc && irc->memb && *(irc->of)) ||
                             (irc->jnc && irc->memb && !*(irc->of))))
                        {
                            *(irc->et) = true;
                            *(irc->lip) = true;
                        }
                    }
                    else if (irc->t == 4)
                    {
                        irc->treset = true;
                    }
                    // Jump to immediate offset
                }
                else if (((irc->jmp && irc->immeda) ||
                          (irc->jz && irc->immeda) ||
                          (irc->jnz && irc->immeda) ||
                          (irc->jm && irc->immeda) ||
                          (irc->jp && irc->immeda) ||
                          (irc->jc && irc->immeda) ||
                          (irc->jnc && irc->immeda) ||
                          (irc->jc && irc->swp) ||
                          (irc->jnc && irc->swp)))
                {
                    if (irc->t == 3)
                    {
                        // Save A
                        *(irc->eacc) = true;
                        *(irc->lrr1) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->ebuff) = true;
                        *(irc->lrr2) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load offset into B
                        *(irc->et) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Load instruction pointer low byte into A
                        *(irc->eip) = true;
                        *(irc->lacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Add A && B && save to temp
                        if (((irc->jmp && irc->immeda) ||
                             (irc->jz && irc->immeda && *(irc->zf)) ||
                             (irc->jnz && irc->immeda && !*(irc->zf)) ||
                             (irc->jm && irc->immeda && *(irc->sf)) ||
                             (irc->jp && irc->immeda && !*(irc->sf)) ||
                             (irc->jc && irc->immeda && *(irc->cf)) ||
                             (irc->jnc && irc->immeda && !*(irc->cf)) ||
                             (irc->jc && irc->swp && *(irc->of)) ||
                             (irc->jnc && irc->swp && !*(irc->of))))
                        {
                            *(irc->ealu) = true;
                            *(irc->lt1) = true;
                            *(irc->sel) = 0;
                        }

                        else
                        {
                            // Just load old IP into temp to avoid jump
                            *(irc->clc) = true;
                            *(irc->lt1) = true;
                            *(irc->eip) = true;
                        }
                    }
                    else if (irc->t == 8)
                    {
                        // Load high byte of IP into A && temp
                        *(irc->lacc) = true;
                        *(irc->lt2) = true;
                        *(irc->eip_b) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Increment high byte of IP if ( carry
                        if (*(irc->xf))
                        {
                            // printf("Carry")
                            *(irc->lt2) = true;
                            *(irc->ealu) = true;
                            if (*(irc->sf))
                            {
                                // Offset was negative, decrement A
                                *(irc->sel) = 5;
                            }
                            else
                            {
                                // Offset was positive, increment A
                                *(irc->sel) = 4;
                            }
                        }
                    }
                    else if (irc->t == 10)
                    {
                        // Set IP to new offset IP
                        *(irc->lip) = true;
                        *(irc->et) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Restore A
                        *(irc->lacc) = true;
                        *(irc->err) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Restore B
                        *(irc->lbuff) = true;
                        *(irc->err_b) = true;
                    }
                    else if (irc->t == 13)
                    {
                        irc->treset = true;
                    }

                    // Jump to Ar offset
                }
                else if (((irc->jmp && irc->immedb) ||
                          (irc->jz && irc->immedb) ||
                          (irc->jnz && irc->immedb) ||
                          (irc->jm && irc->immedb) ||
                          (irc->jp && irc->immedb) ||
                          (irc->jc && irc->immedb) ||
                          (irc->jnc && irc->immedb) ||
                          (irc->jc && irc->shl) ||
                          (irc->jnc && irc->shl)))
                {
                    if (irc->t == 3)
                    {
                        // Save A
                        *(irc->eacc) = true;
                        *(irc->lrr1) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->ebuff) = true;
                        *(irc->lrr2) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load instruction pointer low byte into B
                        *(irc->eip) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Add A && B && save to temp
                        if (((irc->jmp && irc->immedb) ||
                             (irc->jz && irc->immedb && *(irc->zf)) ||
                             (irc->jnz && irc->immedb && !*(irc->zf)) ||
                             (irc->jm && irc->immedb && *(irc->sf)) ||
                             (irc->jp && irc->immedb && !*(irc->sf)) ||
                             (irc->jc && irc->immedb && *(irc->cf)) ||
                             (irc->jnc && irc->immedb && !*(irc->cf)) ||
                             (irc->jc && irc->shl && *(irc->of)) ||
                             (irc->jnc && irc->shl && !*(irc->of))))
                        {
                            *(irc->ealu) = true;
                            *(irc->lt1) = true;
                            *(irc->clc) = true;
                            *(irc->sel) = 0;
                        }
                        else
                        {
                            // Just load old IP into temp to avoid jump
                            *(irc->clc) = true;
                            *(irc->lt1) = true;
                            *(irc->eip) = true;
                        }
                    }
                    else if (irc->t == 7)
                    {
                        // Load high byte of IP into A && temp
                        *(irc->lacc) = true;
                        *(irc->lt2) = true;
                        *(irc->eip_b) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Increment high byte of IP if ( carry
                        if (*(irc->xf))
                        {
                            // printf("Carry")
                            *(irc->lt2) = true;
                            *(irc->ealu) = true;
                            if (*(irc->sf))
                            {
                                // Offset was negative, decrement A
                                *(irc->sel) = 5;
                            }
                            else
                            {
                                // Offset was positive, increment A
                                *(irc->sel) = 4;
                            }
                        }
                    }
                    else if (irc->t == 9)
                    {
                        // Set IP to new offset IP
                        *(irc->lip) = true;
                        *(irc->et) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Restore A
                        *(irc->lacc) = true;
                        *(irc->err) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Restore B
                        *(irc->lbuff) = true;
                        *(irc->err_b) = true;
                    }
                    else if (irc->t == 12)
                    {
                        irc->treset = true;
                    }
                    // Jump to immediate zero-page address
                }
                else if (((irc->jmp && irc->stora) ||
                          (irc->jz && irc->stora) ||
                          (irc->jnz && irc->stora) ||
                          (irc->jm && irc->stora) ||
                          (irc->jp && irc->stora) ||
                          (irc->jc && irc->stora) ||
                          (irc->jnc && irc->stora) ||
                          (irc->jc && irc->shr) ||
                          (irc->jnc && irc->shr)))
                {
                    if (irc->t == 3)
                    {
                        if (((irc->jmp && irc->stora) ||
                             (irc->jz && irc->stora && *(irc->zf)) ||
                             (irc->jnz && irc->stora && !*(irc->zf)) ||
                             (irc->jm && irc->stora && *(irc->sf)) ||
                             (irc->jp && irc->stora && !*(irc->sf)) ||
                             (irc->jc && irc->stora && *(irc->cf)) ||
                             (irc->jnc && irc->stora && !*(irc->cf)) ||
                             (irc->jc && irc->shr && *(irc->of)) ||
                             (irc->jnc && irc->shr && !*(irc->of))))
                        {
                            irc->shouldJump = true;
                        }
                        // Save A
                        *(irc->eacc) = true;
                        *(irc->lrr1) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->ebuff) = true;
                        *(irc->lrr2) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load 0 into T2
                        *(irc->clc) = true;
                        *(irc->lt2) = true;
                        *(irc->data_bus) = 0x0;
                    }
                    else if (irc->t == 6)
                    {
                        // Load temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Read from MEM into B
                        *(irc->ce) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Load lower byte of address to A from T1
                        *(irc->et) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Increment lower byte of address
                        *(irc->clc) = true;
                        *(irc->ealu) = true;
                        *(irc->lt1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 10)
                    {
                        // Load incremented temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Read from MEM into T2
                        *(irc->ce) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Move saved address in B to T1
                        *(irc->ebuff) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Load address in temp reg to address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Load new IP from memory
                        if ((irc->shouldJump))
                        {
                            *(irc->lip) = true;
                            *(irc->ce) = true;
                        }
                    }
                    else if (irc->t == 15)
                    {
                        // Restore A
                        *(irc->lacc) = true;
                        *(irc->err) = true;
                    }
                    else if (irc->t == 16)
                    {
                        // Restore B
                        *(irc->lbuff) = true;
                        *(irc->err_b) = true;
                    }
                    else if (irc->t == 17)
                    {
                        irc->treset = true;
                    }
                    // Jump to zero-page address in Ar
                }
                else if (((irc->jmp && irc->storb) ||
                          (irc->jz && irc->storb) ||
                          (irc->jnz && irc->storb) ||
                          (irc->jm && irc->storb) ||
                          (irc->jp && irc->storb) ||
                          (irc->jc && irc->storb) ||
                          (irc->jnc && irc->storb) ||
                          (irc->jc && irc->deca) ||
                          (irc->jnc && irc->deca)))
                {
                    if (irc->t == 3)
                    {
                        if (((irc->jmp && irc->storb) ||
                             (irc->jz && irc->storb && *(irc->zf)) ||
                             (irc->jnz && irc->storb && !*(irc->zf)) ||
                             (irc->jm && irc->storb && *(irc->sf)) ||
                             (irc->jp && irc->storb && !*(irc->sf)) ||
                             (irc->jc && irc->storb && *(irc->cf)) ||
                             (irc->jnc && irc->storb && !*(irc->cf)) ||
                             (irc->jc && irc->deca && *(irc->of)) ||
                             (irc->jnc && irc->deca && !*(irc->of))))
                        {
                            irc->shouldJump = true;
                        }
                        // Save A && load A into T1
                        *(irc->eacc) = true;
                        *(irc->lrr1) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->ebuff) = true;
                        *(irc->lrr2) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load 0 into T2
                        *(irc->clc) = true;
                        *(irc->lt2) = true;
                        *(irc->data_bus) = 0x0;
                    }
                    else if (irc->t == 6)
                    {
                        // Load temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Read from MEM into B
                        *(irc->ce) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Load lower byte of address to A from RR1
                        *(irc->err) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Increment lower byte of address
                        *(irc->ealu) = true;
                        *(irc->lt1) = true;
                        *(irc->clc) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 10)
                    {
                        // Load incremented temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Read from MEM into T2
                        *(irc->ce) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Move saved address in B to T1
                        *(irc->ebuff) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Load address in temp reg to address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Load new IP from memory
                        if ((irc->shouldJump))
                        {
                            *(irc->lip) = true;
                            *(irc->ce) = true;
                        }
                    }
                    else if (irc->t == 15)
                    {
                        // Restore A
                        *(irc->lacc) = true;
                        *(irc->err) = true;
                    }
                    else if (irc->t == 16)
                    {
                        // Restore B
                        *(irc->lbuff) = true;
                        *(irc->err_b) = true;
                    }
                    else if (irc->t == 17)
                    {
                        irc->treset = true;
                    }

                    // No operand ALU operations
                }
                else if (((irc->log && irc->shl) ||
                          (irc->log && irc->shr) ||
                          (irc->log && irc->inca) ||
                          (irc->log && irc->incb) ||
                          (irc->log && irc->deca) ||
                          (irc->log && irc->decb) ||
                          (irc->log && irc->mema) ||
                          (irc->log && irc->memb) ||
                          (irc->log && irc->immeda) ||
                          (irc->log && irc->immedb)))
                {
                    if (irc->t == 3)
                    {
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        if (irc->log && irc->shl)
                        {
                            // Left shift
                            *(irc->sel) = 2;
                        }
                        else if (irc->log && irc->shr)
                        {
                            // Right shift
                            *(irc->sel) = 3;
                        }
                        else if (irc->log && irc->inca)
                        {
                            // Increment A
                            *(irc->sel) = 4;
                        }
                        else if (irc->log && irc->deca)
                        {
                            // Decrement A
                            *(irc->sel) = 5;
                        }
                        else if (irc->log && irc->incb)
                        {
                            // Increment B
                            *(irc->sel) = 6;
                            *(irc->lacc) = false;
                            *(irc->lbuff) = true;
                        }
                        else if (irc->log && irc->decb)
                        {
                            // Decrement B
                            *(irc->sel) = 7;
                            *(irc->lacc) = false;
                            *(irc->lbuff) = true;
                        }
                        else if (irc->log && irc->mema)
                        {
                            // && A && B
                            *(irc->sel) = 8;
                        }
                        else if (irc->log && irc->memb)
                        {
                            // || A && B
                            *(irc->sel) = 9;
                        }
                        else if (irc->log && irc->immeda)
                        {
                            // XOR A && B
                            *(irc->sel) = 0xA;
                        }
                        else if (irc->log && irc->immedb)
                        {
                            // ! A
                            *(irc->sel) = 0xB;
                        }
                        else if (irc->t == 4)
                        {
                            irc->treset = true;
                        }
                    }

                    // One operand ALU operations
                }
                else if (((irc->log && irc->stora) ||
                          (irc->log && irc->storb) ||
                          (irc->log && irc->swp)))
                {
                    if (irc->t == 3)
                    {
                        // Save B reg
                        *(irc->ebuff) = true;
                        *(irc->lrr1) = true;
                    }
                    else if (irc->t == 4)
                    {
                        *(irc->et) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        if (irc->log && irc->stora)
                        {
                            // && immed
                            *(irc->sel) = 8;
                        }
                        else if (irc->log && irc->storb)
                        {
                            // || immed
                            *(irc->sel) = 9;
                        }
                        else if (irc->log && irc->swp)
                        {
                            // XOR immed
                            *(irc->sel) = 0xA;
                        }
                    }
                    else if (irc->t == 6)
                    {
                        // Restore B reg
                        *(irc->lbuff) = true;
                        *(irc->err) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 7)
                    {
                        irc->treset = true;
                    }

                    // TODO: Fix IO
                    // IO A
                }
                else if (irc->io && irc->mema)
                {
                    if (irc->t == 3)
                    {
                        irc->treset = true;
                        printf("Clock cycles: %d\n", totalCycles);
                        printf("A REG: %02X\n", acc->data);
                        printf("--------------\n");
                    }

                    // IO B
                }
                else if (irc->io && irc->memb)
                {
                    if (irc->t == 3)
                    {
                        irc->treset = true;
                        printf("Clock cycles: %d\n", totalCycles);
                        printf("B REG: %02X\n", buff->data);
                        printf("--------------\n");
                    }
                    // CALL Function
                }
                else if (irc->jz && irc->incb)
                {
                    if (irc->t == 3)
                    {
                        // Save A
                        *(irc->lrr1) = true;
                        *(irc->eacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->lrr2) = true;
                        *(irc->ebuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        //// Load low byte of stack pointer into A
                        *(irc->lacc) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Load high byte of stack pointer into B
                        *(irc->esp_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Increment lower byte of stack pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 8)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 9)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Write lower byte of IP to stack
                        *(irc->we) = true;
                        *(irc->eip) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Increment lower byte of stack pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 12)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 13)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Write upper byte of IP to stack
                        *(irc->we) = true;
                        *(irc->eip_b) = true;
                    }
                    else if (irc->t == 15)
                    {
                        // Increment lower byte of stack pointer in A

                        // printf(hex(*(irc->data_bus)))
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 16)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 17)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 18)
                    {
                        // Save lower byte of BP to stack
                        *(irc->we) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 19)
                    {
                        // Increment lower byte of stack pointer in A
                        // printf("CALL saved lower BP) { " + hex(*(irc->data_bus)))
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 20)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 21)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 22)
                    {
                        // Save upper byte of BP to stack
                        // printf("CALL set new SP) { " + hex(*(irc->adr_bus)))
                        *(irc->we) = true;
                        *(irc->ebp_b) = true;
                    }
                    else if (irc->t == 23)
                    {
                        // Set BP to SP
                        // printf("CALL saved upper BP) { " + hex(*(irc->data_bus)))
                        *(irc->lbpa) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 24)
                    {
                        // Set IP to be call address
                        // printf("CALL set new BP) { " + hex(*(irc->adr_bus)))
                        *(irc->lip) = true;
                        *(irc->et) = true;
                    }
                    else if (irc->t == 25)
                    {
                        // Restore A
                        *(irc->err) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 26)
                    {
                        // Restore B
                        *(irc->err_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 27)
                    {
                        // Call finished
                        irc->treset = true;
                    }
                    // CALLZ <immed>
                }
                else if (irc->jnz && irc->incb)
                {
                    if (irc->t == 3)
                    {
                        // Save A
                        *(irc->lrr1) = true;
                        *(irc->eacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->lrr2) = true;
                        *(irc->ebuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load 0 into T2
                        *(irc->clc) = true;
                        *(irc->lt2) = true;
                        *(irc->data_bus) = 0x0;
                    }
                    else if (irc->t == 6)
                    {
                        // Load temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Read from MEM into B
                        *(irc->ce) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Load lower byte of address to A from T1
                        // printf(hex(*(irc->data_bus)))
                        *(irc->et) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Increment lower byte of address
                        *(irc->clc) = true;
                        *(irc->ealu) = true;
                        *(irc->lt1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 10)
                    {
                        // Load incremented temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Read from MEM into T2
                        *(irc->ce) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Move saved address in B to T1
                        *(irc->ebuff) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 13)
                    {
                        //// Load low byte of stack pointer into A
                        *(irc->lacc) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Load high byte of stack pointer into B
                        *(irc->esp_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 15)
                    {
                        // Increment lower byte of stack pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 16)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 17)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 18)
                    {
                        // Write lower byte of IP to stack
                        *(irc->we) = true;
                        *(irc->eip) = true;
                    }
                    else if (irc->t == 19)
                    {
                        // Increment lower byte of stack pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 20)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 21)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 22)
                    {
                        // Write upper byte of IP to stack
                        *(irc->we) = true;
                        *(irc->eip_b) = true;
                    }
                    else if (irc->t == 23)
                    {
                        // Increment lower byte of stack pointer in A

                        // printf(hex(*(irc->data_bus)))
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 24)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 25)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 26)
                    {
                        // Save lower byte of BP to stack
                        *(irc->we) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 27)
                    {
                        // Increment lower byte of stack pointer in A
                        // printf("CALL saved lower BP) { " + hex(*(irc->data_bus)))
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 28)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 29)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 30)
                    {
                        // Save upper byte of BP to stack
                        *(irc->we) = true;
                        *(irc->ebp_b) = true;
                    }
                    else if (irc->t == 31)
                    {
                        // Set BP to SP
                        *(irc->lbpa) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 32)
                    {
                        // Set IP to be call address
                        *(irc->lip) = true;
                        *(irc->et) = true;
                    }
                    else if (irc->t == 33)
                    {
                        // Restore A
                        *(irc->err) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 34)
                    {
                        // Restore B
                        *(irc->err_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 35)
                    {
                        // Call finished
                        irc->treset = true;
                    }
                    // CALLZ Ar
                }
                else if (irc->jnz && irc->aux)
                {
                    if (irc->t == 3)
                    {
                        // Save A && load A into T1
                        *(irc->lrr1) = true;
                        *(irc->lt1) = true;
                        *(irc->eacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->lrr2) = true;
                        *(irc->ebuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load 0 into T2
                        *(irc->clc) = true;
                        *(irc->lt2) = true;
                        *(irc->data_bus) = 0x0;
                    }
                    else if (irc->t == 6)
                    {
                        // Load temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Read from MEM into B
                        *(irc->ce) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Load lower byte of address to A from T1
                        // printf(hex(*(irc->data_bus)))
                        *(irc->et) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Increment lower byte of address
                        *(irc->clc) = true;
                        *(irc->ealu) = true;
                        *(irc->lt1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 10)
                    {
                        // Load incremented temp into address reg
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Read from MEM into T2
                        *(irc->ce) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Move saved address in B to T1
                        *(irc->ebuff) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 13)
                    {
                        //// Load low byte of stack pointer into A
                        *(irc->lacc) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Load high byte of stack pointer into B
                        *(irc->esp_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 15)
                    {
                        // Increment lower byte of stack pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 16)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 17)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 18)
                    {
                        // Write lower byte of IP to stack
                        *(irc->we) = true;
                        *(irc->eip) = true;
                    }
                    else if (irc->t == 19)
                    {
                        // Increment lower byte of stack pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 20)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 21)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 22)
                    {
                        // Write upper byte of IP to stack
                        *(irc->we) = true;
                        *(irc->eip_b) = true;
                    }
                    else if (irc->t == 23)
                    {
                        // Increment lower byte of stack pointer in A

                        // printf(hex(*(irc->data_bus)))
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 24)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 25)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 26)
                    {
                        // Save lower byte of BP to stack
                        *(irc->we) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 27)
                    {
                        // Increment lower byte of stack pointer in A
                        // printf("CALL saved lower BP) { " + hex(*(irc->data_bus)))
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 28)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 29)
                    {
                        // Load new SP into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 30)
                    {
                        // Save upper byte of BP to stack
                        *(irc->we) = true;
                        *(irc->ebp_b) = true;
                    }
                    else if (irc->t == 31)
                    {
                        // Set BP to SP
                        *(irc->lbpa) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 32)
                    {
                        // Set IP to be call address
                        *(irc->lip) = true;
                        *(irc->et) = true;
                    }
                    else if (irc->t == 33)
                    {
                        // Restore A
                        *(irc->err) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 34)
                    {
                        // Restore B
                        *(irc->err_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 35)
                    {
                        // Call finished
                        irc->treset = true;
                    }
                    // Return from Function
                }
                else if (irc->jz && irc->aux)
                {
                    if (irc->t == 3)
                    {
                        // Save A
                        *(irc->lrr1) = true;
                        *(irc->eacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        // printf ("Saved A) { " + hex(*(irc->data_bus)))
                        *(irc->lrr2) = true;
                        *(irc->ebuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        //// Load low byte of base pointer into A
                        // printf ("Saved B) { " + hex(*(irc->data_bus)))
                        *(irc->lacc) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Load high byte of base pointer into B
                        *(irc->ebp_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Load BP into address register
                        *(irc->ladd) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Load upper byte of BP from stack into T2
                        *(irc->ce) = true;
                        *(irc->lt2) = true;
                        // printf ("SP into ADR) { " + hex(*(irc->adr_bus)))
                    }
                    else if (irc->t == 9)
                    {
                        // Decrement lower byte of base pointer in A
                        // printf("RET restored upper BP) { " + hex(*(irc->data_bus)))
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lbp1) = true;
                        *(irc->sel) = 5;
                    }
                    else if (irc->t == 10)
                    {
                        // Decrement upper byte of base pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lbp2) = true;
                            *(irc->sel) = 7;
                        }
                    }
                    else if (irc->t == 11)
                    {
                        // Load BP into address register
                        *(irc->ladd) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Load lower byte of BP from stack into T1
                        *(irc->ce) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Decrement lower byte of base pointer in A
                        // printf("RET restored lower BP) { " + hex(*(irc->data_bus)))
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lbp1) = true;
                        *(irc->sel) = 5;
                    }
                    else if (irc->t == 14)
                    {
                        // Decrement upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lbp2) = true;
                            *(irc->sel) = 7;
                        }
                    }
                    else if (irc->t == 15)
                    {
                        // Load BP into address register
                        *(irc->ladd) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 16)
                    {
                        // Load upper byte of IP from stack
                        *(irc->ce) = true;
                        *(irc->lip2) = true;
                    }
                    else if (irc->t == 17)
                    {
                        // Decrement lower byte of base pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lbp1) = true;
                        *(irc->sel) = 5;
                    }
                    else if (irc->t == 18)
                    {
                        // Decrement upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lbp2) = true;
                            *(irc->sel) = 7;
                        }
                    }
                    else if (irc->t == 19)
                    {
                        // Load BP into address register
                        *(irc->ladd) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 20)
                    {
                        // Load lower byte of IP from stack
                        *(irc->ce) = true;
                        *(irc->lip1) = true;
                    }
                    else if (irc->t == 21)
                    {
                        // Decrement lower byte of base pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lbp1) = true;
                        *(irc->sel) = 5;
                    }
                    else if (irc->t == 22)
                    {
                        // Decrement upper byte of base pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lbp2) = true;
                            *(irc->sel) = 7;
                        }
                    }
                    else if (irc->t == 23)
                    {
                        // Set SP to decremented BP
                        *(irc->ebp) = true;
                        *(irc->lspa) = true;
                    }
                    else if (irc->t == 24)
                    {
                        // Set BP to new saved BP in T
                        *(irc->et) = true;
                        *(irc->lbpa) = true;
                    }
                    else if (irc->t == 25)
                    {
                        // Restore A
                        // printf("RET restored BP) { " + hex(*(irc->adr_bus)))
                        *(irc->err) = true;
                        *(irc->lacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 26)
                    {
                        // Restore B
                        // printf ("Restored A) { " + hex(*(irc->data_bus)))
                        *(irc->err_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 27)
                    {
                        // Call finished
                        // printf ("Restored B) { " + hex(*(irc->data_bus)))
                        irc->treset = true;
                    }
                    // Peek at <immed> BP offset
                }
                else if (irc->jmp && irc->shl)
                {
                    if (irc->t == 3)
                    {
                        // Save B
                        *(irc->lrr1) = true;
                        *(irc->ebuff) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Load low byte of base pointer into A
                        *(irc->lacc) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load offset into B
                        *(irc->lbuff) = true;
                        *(irc->et) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Add A && B
                        *(irc->lacc) = true;
                        *(irc->ealu) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 7)
                    {
                        // Move result to temp1
                        *(irc->eacc) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Load BP2 into A
                        *(irc->ebp_b) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Decide if ( upper byte of BP needs to be incremented
                        // printf("BP_B) { " + hex(*(irc->data_bus)))
                        if (*(irc->xf))
                        {
                            // printf("Carry")
                            *(irc->lacc) = true;
                            *(irc->ealu) = true;
                            if (*(irc->sf))
                            {
                                // Offset was negative, decrement A
                                *(irc->sel) = 5;
                            }
                            else
                            {
                                // Offset was positive, increment A
                                *(irc->sel) = 4;
                            }
                        }
                    }
                    else if (irc->t == 10)
                    {
                        // Move result to temp2
                        *(irc->eacc) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Move temp into address reg
                        // printf("ACC) { " + hex(*(irc->data_bus)))
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Move output into A
                        *(irc->lacc) = true;
                        *(irc->ce) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Restore B
                        *(irc->err) = true;
                        *(irc->lbuff) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Call finished
                        *(irc->clc) = false;
                        irc->treset = true;
                    }
                    // Peek at B reg BP offset
                }
                else if (irc->jmp && irc->aux)
                {
                    // printf("A reg peek")
                    if (irc->t == 3)
                    {
                        // Save A
                        *(irc->lrr1) = true;
                        *(irc->eacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->lrr2) = true;
                        *(irc->ebuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load low byte of base pointer into A
                        *(irc->lacc) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Load offset into B
                        *(irc->lbuff) = true;
                        *(irc->err_b) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Add A && B
                        // printf("Offset) { " + hex(*(irc->data_bus)))
                        *(irc->lacc) = true;
                        *(irc->ealu) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 8)
                    {
                        // Move result to temp1
                        *(irc->eacc) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Load BP2 into A
                        *(irc->ebp_b) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Decide if ( upper byte of BP needs to be incremented
                        // printf("BP_B) { " + hex(*(irc->data_bus)))
                        if (*(irc->xf))
                        {
                            // printf("Carry")
                            *(irc->lacc) = true;
                            *(irc->ealu) = true;
                            if (*(irc->sf))
                            {
                                // Offset was negative, decrement A
                                *(irc->sel) = 5;
                            }
                            else
                            {
                                // Offset was positive, increment A
                                *(irc->sel) = 4;
                            }
                        }
                    }
                    else if (irc->t == 11)
                    {
                        // Move result to temp2
                        *(irc->eacc) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Move temp into address reg
                        // printf("ACC) { " + hex(*(irc->data_bus)))
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Move output into A
                        *(irc->lacc) = true;
                        *(irc->ce) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Restore B
                        *(irc->err_b) = true;
                        *(irc->lbuff) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 15)
                    {
                        // Call finished
                        irc->treset = true;
                    }
                    // Poke A to <immed> BP offset
                }
                else if (irc->jmp && irc->shr)
                {
                    if (irc->t == 3)
                    {
                        // Save A to RR2
                        *(irc->eacc) = true;
                        *(irc->lrr2) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B to RR1
                        // printf("Saved A) { " + hex(*(irc->data_bus)))
                        *(irc->lrr1) = true;
                        *(irc->ebuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load low byte of base pointer into A
                        *(irc->lacc) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Load offset into B
                        *(irc->lbuff) = true;
                        *(irc->et) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Add A && B
                        *(irc->lacc) = true;
                        *(irc->ealu) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 8)
                    {
                        // Move result to temp1
                        *(irc->eacc) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Load BP2 into A
                        *(irc->ebp_b) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Decide if ( upper byte of BP needs to be incremented
                        // printf("BP_B) { " + hex(*(irc->data_bus)))
                        if (*(irc->xf))
                        {
                            // printf("Carry")
                            *(irc->lacc) = true;
                            *(irc->ealu) = true;
                            if (*(irc->sf))
                            {
                                // Offset was negative, decrement A
                                *(irc->sel) = 5;
                            }
                            else
                            {
                                // Offset was positive, increment A
                                *(irc->sel) = 4;
                            }
                        }
                    }
                    else if (irc->t == 11)
                    {
                        // Move result to temp2
                        *(irc->eacc) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Move temp into address reg
                        // printf("ACC) { " + hex(*(irc->data_bus)))
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Write saved value of A && restore A
                        *(irc->err_b) = true;
                        *(irc->we) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 14)
                    {
                        // Restore B
                        // printf("Saved A) { " + hex(*(irc->data_bus)))
                        *(irc->err) = true;
                        *(irc->lbuff) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 15)
                    {
                        // Call finished
                        irc->treset = true;
                        // printf("finish poke")
                    }
                    // Poke A to B reg BP offset
                }
                else if (irc->jmp && irc->inca)
                {
                    if (irc->t == 3)
                    {
                        // Save A to RR2
                        *(irc->eacc) = true;
                        *(irc->lrr2) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B to RR1
                        // printf("Saved A) { " + hex(*(irc->data_bus)))
                        *(irc->lrr1) = true;
                        *(irc->ebuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load low byte of base pointer into A
                        *(irc->lacc) = true;
                        *(irc->ebp) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Add A && B
                        *(irc->lacc) = true;
                        *(irc->ealu) = true;
                        *(irc->sel) = 0;
                    }
                    else if (irc->t == 7)
                    {
                        // Move result to temp1
                        *(irc->eacc) = true;
                        *(irc->lt1) = true;
                    }
                    else if (irc->t == 8)
                    {
                        // Load BP2 into A
                        *(irc->ebp_b) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 9)
                    {
                        // Decide if ( upper byte of BP needs to be incremented
                        // printf("BP_B) { " + hex(*(irc->data_bus)))
                        if (*(irc->xf))
                        {
                            // printf("Carry")
                            *(irc->lacc) = true;
                            *(irc->ealu) = true;
                            if (*(irc->sf))
                            {
                                // Offset was negative, decrement A
                                *(irc->sel) = 5;
                            }
                            else
                            {
                                // Offset was positive, increment A
                                *(irc->sel) = 4;
                            }
                        }
                    }
                    else if (irc->t == 10)
                    {
                        // Move result to temp2
                        *(irc->eacc) = true;
                        *(irc->lt2) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Move temp into address reg
                        // printf("ACC) { " + hex(*(irc->data_bus)))
                        *(irc->et) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Write saved value of A && restore A
                        *(irc->err_b) = true;
                        *(irc->we) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Call finished
                        irc->treset = true;
                        // printf("finish poke")
                    }
                    // Pop from SP
                }
                else if (irc->jmp && irc->deca)
                {
                    if (irc->t == 3)
                    {
                        // Save B
                        *(irc->lrr1) = true;
                        *(irc->ebuff) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Load stack pointer into address reg && A
                        *(irc->lacc) = true;
                        *(irc->esp) = true;
                        *(irc->ladd) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Move output into RR2
                        *(irc->lrr2) = true;
                        *(irc->ce) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Load high byte of stack pointer into B
                        *(irc->esp_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Decrement lower byte of stack pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 5;
                    }
                    else if (irc->t == 8)
                    {
                        // Decrement upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 7;
                        }
                    }
                    else if (irc->t == 9)
                    {
                        // Move saved value from RR2 to A
                        *(irc->err_b) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Restore B
                        *(irc->err) = true;
                        *(irc->lbuff) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Pop finished
                        irc->treset = true;
                    }
                    // Push A reg to SP
                }
                else if (irc->jmp && irc->decb)
                {
                    if (irc->t == 3)
                    {
                        // Save A
                        *(irc->lrr1) = true;
                        *(irc->eacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->lrr2) = true;
                        *(irc->ebuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load stack pointer lower byte into A
                        *(irc->lacc) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Load high byte of stack pointer into B
                        *(irc->esp_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Increment lower byte of stack pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 8)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 9)
                    {
                        // Load stack pointer into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Write saved A in RR1 to SP && restore A
                        *(irc->err) = true;
                        *(irc->we) = true;
                        *(irc->lacc) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Restore B
                        *(irc->err_b) = true;
                        *(irc->lbuff) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Push finished
                        irc->treset = true;
                        // printf("Finish reg push")
                    }
                    // Push <immed> to SP
                }
                else if (irc->jmp && irc->swp)
                {
                    if (irc->t == 3)
                    {
                        // Save A
                        *(irc->lrr1) = true;
                        *(irc->eacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 4)
                    {
                        // Save B
                        *(irc->lrr2) = true;
                        *(irc->ebuff) = true;
                    }
                    else if (irc->t == 5)
                    {
                        // Load stack pointer lower byte into A
                        *(irc->lacc) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 6)
                    {
                        // Load high byte of stack pointer into B
                        *(irc->esp_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 7)
                    {
                        // Increment lower byte of stack pointer in A
                        *(irc->ealu) = true;
                        *(irc->lacc) = true;
                        *(irc->lsp1) = true;
                        *(irc->sel) = 4;
                    }
                    else if (irc->t == 8)
                    {
                        // Increment upper byte of stack pointer in B if ( carry
                        if (*(irc->cf))
                        {
                            *(irc->lbuff) = true;
                            *(irc->ealu) = true;
                            *(irc->lsp2) = true;
                            *(irc->sel) = 6;
                        }
                    }
                    else if (irc->t == 9)
                    {
                        // Load stack pointer into address register
                        *(irc->ladd) = true;
                        *(irc->esp) = true;
                    }
                    else if (irc->t == 10)
                    {
                        // Write <immed> to SP
                        *(irc->et) = true;
                        *(irc->we) = true;
                    }
                    else if (irc->t == 11)
                    {
                        // Restore A
                        *(irc->err) = true;
                        *(irc->lacc) = true;
                        *(irc->clc) = true;
                    }
                    else if (irc->t == 12)
                    {
                        // Restore B
                        *(irc->err_b) = true;
                        *(irc->lbuff) = true;
                    }
                    else if (irc->t == 13)
                    {
                        // Push finished
                        irc->treset = true;
                    }
                }
            }
        }
        
    }
    irc->prevclk = *(irc->clk);
    //printf("Toggle prevclk");
    // always @ *
    // irc->SetOpcodes()
}