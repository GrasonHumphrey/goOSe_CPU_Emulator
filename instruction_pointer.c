#include "instruction_pointer.h"

const int CODE_START_LOC = 0x100;

void Update_Instruction_Pointer(Instruction_Pointer *ip)
{
        if ((!ip->prevclk) && (*(ip->clk)))
        {
            if (*(ip->reset))
            {
                ip->adr = CODE_START_LOC;
            }
            if (*(ip->count))
            {
                ip->adr += 1;
            }
            if (*(ip->lip))
            {
                if (*(ip->adr_bus) == -1)
                {
                    printf("WARNING: Attempt load IP with unassigned adr_bus");
                }
                ip->adr = *(ip->adr_bus);
            }
            if (*(ip->lip1))
            {
                if (*(ip->data_bus) == -1)
                {
                    printf("WARNING: Attempt to load IP with unassigned data bus");
                }
                ip->adr = (*(ip->adr_bus) & 0xFF00) | *(ip->data_bus);
            }
            if (*(ip->lip2))
            {
                if (*(ip->data_bus) == -1)
                {
                    printf("WARNING: Attempt to load IP with unassigned data bus\n");
                }
                ip->adr = (*(ip->adr_bus) & 0x00FF) | (*(ip->data_bus) << 8);
            }
        }
        ip->prevclk = *(ip->clk);

        if (*(ip->eip))
        {
            if (ip->adr == -1)
            {
                printf("WARNING: IP attempt set adr_bus with unassigned adr\n");
            }
            *(ip->adr_bus) = ip->adr;
            *(ip->data_bus) = ip->adr & 0x00FF;
        }
        if (*(ip->eip_b))
        {
            *(ip->adr_bus) = ip->adr;
            *(ip->data_bus) = (ip->adr & 0xFF00) >> 8;
        }
        ip->prevclk = *(ip->clk);
}