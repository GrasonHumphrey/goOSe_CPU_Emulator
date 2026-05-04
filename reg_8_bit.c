#include "reg_8_bit.h"

void Update_Reg_8_Bit(Reg_8_Bit *reg)
{
    if ((!reg->prevclk) && (*(reg->clk)))
    {
        if (*(reg->lab))
        {
            if (*(reg->data_bus) == -1)
            {
                printf("WARNING: AB Reg attempt write to data with unassigned data_bus\n");
            }
            reg->data = *(reg->data_bus);
            //printf("AB Load: " + str(reg->data));
        }
    }
    reg->prevclk = *(reg->clk);
    if (*(reg->eab))
    {
        *(reg->data_bus) = reg->data;
        //printf("AB Out: " + str(reg->data));
    }
    *(reg->alt_out) = reg->data;
}