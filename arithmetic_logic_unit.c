#include "arithmetic_logic_unit.h"

void Update_ALU(Arithmetic_Logic_Unit *alu)
{
    if (*(alu->clk))
    {
        bool overrideSF = false;
        if (*(alu->clc))
        {
            *(alu->cf) = false;
            *(alu->of) = false;
            *(alu->xf) = false;
        }
        if (*(alu->sel) == 0x0)
        {
            // ADD
            int result = (*(alu->alu_in_a) + *(alu->alu_in_b));
                //printf(hex(result);
            
            alu->data = result & 0xFF;
            
            if (*(alu->ealu))
            {
                //printf("Add result: " + hex(result));
                if (*(alu->cf))
                {
                    result += 1;
                    alu->data = result & 0xFF;
                    //printf("carry");
                }
                //printf("Add result: " + hex(alu->data));
                // Calculate carry and overflow flags
                // Set overflow flag if result is incorrect for signed arithmetic
                *(alu->of) = (result > 0x7F) || (result < -0x7F);
                // Set carry flag if result is incorrect for unsigned arithmetic
                *(alu->cf) = result > 0xFF;
                //printf(hex(result));
                //printf(alu->cf);
                // XF for carry needed with unsigned A and signed B
                *(alu->xf) = !((*(alu->alu_in_b) <= 0x7F && result <= 0xFF) || (*(alu->alu_in_b) > 0x7F && result > 0xFF));
                if (*(alu->xf))
                {
                    overrideSF = true;
                    *(alu->sf) = *(alu->alu_in_b) > 0x7F;
                }
            }
        }
        if (*(alu->sel) == 0x1)
        {
            // SUBTRACT
            int result = (*(alu->alu_in_a) - *(alu->alu_in_b));
            alu->data = result & 0xFF;
            if (*(alu->ealu))
            {
                if (*(alu->cf))
                {
                    result -= 1;
                    alu->data = result & 0xFF;
                }
                // Calculate carry and overflow flags
                // Set overflow flag if result is incorrect for signed arithmetic
                *(alu->of) = (result > 0x7F) || (result < -0x7F);
                // Set carry flag if result is incorrect for unsigned arithmetic
                *(alu->cf) = result < 0;
                // XF for carry needed with unsigned A and signed B
                *(alu->xf) = !((*(alu->alu_in_b) <= 0x7F && result <= 0xFF) || (*(alu->alu_in_b) > 0x7F && result > 0xFF));
                if (*(alu->xf))
                {
                    overrideSF = true;
                    *(alu->sf) = *(alu->alu_in_b) > 0x7F;
                }
            }
        }
        if (*(alu->sel) == 0x2){
            // Bit shift left
            //result = (alu->alu_in_a << alu->alu_in_b)
            int result = (*(alu->alu_in_a) << 1);
            alu->data = result & 0xFF;
            *(alu->cf) = result > 0xFF;
        }
        if (*(alu->sel) == 0x3){
            // Bit shift right
            //result = (*(alu->alu_in_a) >> alu->alu_in_b)
            int result = (*(alu->alu_in_a) >> 1);
            alu->data = result & 0xFF;
            *(alu->cf) = result < 0;
        }
        if (*(alu->sel) == 0x4){
            // Increment A
            int result = *(alu->alu_in_a) + 1;
            alu->data = result & 0xFF;
            if (*(alu->ealu)){
                *(alu->of) = (result > 0x7F) || (result < -0x7F);
                *(alu->cf) = result > 0xFF;
            }
        }
        if (*(alu->sel) == 0x5){
            // Decrement A
            int result = *(alu->alu_in_a) - 1;
            alu->data = result & 0xFF;
            if (*(alu->ealu)){
                *(alu->of) = (result > 0x7F) || (result < -0x7F);
                *(alu->cf) = result < 0;
            }
        }
        if (*(alu->sel) == 0x6){
            // Increment B
            int result = *(alu->alu_in_b) + 1;
            alu->data = result & 0xFF;
            if (*(alu->ealu)){
                *(alu->of) = (result > 0x7F) || (result < -0x7F);
                *(alu->cf) = result > 0xFF;
            }
        }
        if (*(alu->sel) == 0x7){
            // Decrement B
            int result = *(alu->alu_in_b) - 1;
            alu->data = result & 0xFF;
            if (*(alu->ealu)){
                *(alu->of) = (result > 0x7F) || (result < -0x7F);
                *(alu->cf) = result < 0;
            }
        }
        if (*(alu->sel) == 0x8){
            // AND A and B
            alu->data = *(alu->alu_in_a) & *(alu->alu_in_b);
        }
        if (*(alu->sel) == 0x9){
            // OR A and B
            alu->data = *(alu->alu_in_a) | *(alu->alu_in_b);
        }
        if (*(alu->sel) == 0xA){
            // XOR A and B
            alu->data = *(alu->alu_in_a) ^ *(alu->alu_in_b);
            //print("A: " + str(*(alu->alu_in_a)))
            //print("B: " + str(*(alu->alu_in_b)))
            //print("Data: " + str(alu->data))
        }
        if (*(alu->sel) == 0xB){
            // NOT A
            alu->data = (~*(alu->alu_in_a)) & 0xFF;
        }
        if (*(alu->sel) == 0xC){
            // NOT B
            alu->data = (~*(alu->alu_in_b)) & 0xFF;
        }
        if (*(alu->ealu)){
            *(alu->data_bus) = alu->data;
            //print(alu->data_bus)
            // Zero flag is set if result is zero
            *(alu->zf) = (alu->data == 0);
            //print("ALU data: " + hex(alu->data))
            //print("ZF: " + str(alu->zf))
            //print
            // Sign flag is set if result is less than zero
            if (!overrideSF)
            {
                *(alu->sf) = alu->data & 0xFF > 0x7F;
                //print("EALU SF: " + str(alu->sf))
            }
        }
    }
}