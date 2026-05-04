#include "reg_16_bit.h"

void Update_Reg_16_Bit(Reg_16_Bit *reg)
{
    if ((!reg->prevclk) && (*(reg->clk)))
    {
        if (*(reg->lt1))
        {
            if (*(reg->data_bus) == -1)
            {
                printf("WARNING: Temp Reg attempt to load with unassigned data bus\n");
            }
            reg->adr = ((reg->adr) & 0xFF00) | *(reg->data_bus);
            //printf("TR Load: " + hex(reg->adr));
        }
        if (*(reg->lt2))
        {
            if (*(reg->data_bus) == -1)
            {
                printf("WARNING: Temp Reg attempt to load with unassigned data bus\n");
            }
            reg->adr = ((reg->adr) & 0x00FF) | (*(reg->data_bus) << 8);
            //printf("TR2 Load: " + hex(reg->data_bus));
        }
        if (*(reg->lta))
        {
            if (*(reg->adr_bus) == -1)
            {
                printf("WARNING: Temp Reg attempt to load with unassigned adr bus\n");
            }
            reg->adr = *(reg->adr_bus);
        }
    }
    reg->prevclk = *(reg->clk);
    if (*(reg->et))
    {
        *(reg->adr_bus) = reg->adr;
        *(reg->data_bus) = reg->adr & 0x00FF;
        //printf("TR Data Out: " + hex(reg->adr & 0x00FF));
        //printf("TR Adr Out: " + hex(reg->adr));
    }
    if (*(reg->et_b))
    {
        *(reg->adr_bus) = reg->adr;
        *(reg->data_bus) = (reg->adr & 0xFF00) >> 8;
        //printf("TR Data Out: " + hex((reg->adr & 0xFF00) >> 8));
    }
}