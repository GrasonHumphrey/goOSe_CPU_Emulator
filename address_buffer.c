#include "address_buffer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void LoadMemoryFromFile()
{
    // TODO: Figure this out
    /*
        f = open("compiled_output.txt", "r")
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            adr_buf->memory[int(parts)] = int(parts[1], 16)

        # Set up key buffer memory
        adr_buf->memory[KEY_BUF_PTR_LOC] = (KEY_BUF_BASE+0x1F) & 0xFF
        #print("Init KEY_BUF_PTR_LOC: " + hex((KEY_BUF_BASE+0x1F) & 0xFF))
        adr_buf->memory[KEY_BUF_PTR_LOC+1] = ((KEY_BUF_BASE+0x1F) & 0xFF00) >> 8
        #print("Init KEY_BUF_PTR_LOC+1: " + hex(((KEY_BUF_BASE+0x1F) & 0xFF00) >> 8))

        #print(adr_buf->memory)

        */
}

void Load_Memory_From_File(Address_Buffer *adr_buf)
{
    FILE *fp = fopen("compiled_output.txt", "r");
    if (fp == NULL)
    {
        perror("Error opening file");
        return;
    }

    char buffer[256]; // Adjust size based on expected max line length
    while (fgets(buffer, sizeof(buffer), fp))
    {
        //printf("%s", buffer); // Each line already includes the '\n'
        char *token;
        // First part is address, stored in decimal
        token = strtok(buffer, " ");
        int address = (int)strtol(token, NULL, 10);
        // Second part is data, stored in hex
        token = strtok(NULL, " ");
        int data = (int)strtol(token, NULL, 16);
        adr_buf->memory[address] = data;
        //printf("memory[%d] = %d\n", address, data);
    }

    fclose(fp);
    return;
}

void Update_Address_Buffer(Address_Buffer *adr_buf)
{
    if ((!adr_buf->prevclk) && (*(adr_buf->clk)))
    {
        if (*(adr_buf->reset))
        {
            LoadMemoryFromFile();
            adr_buf->adr = 0;
        }
        if (*(adr_buf->ladd))
        {
            if (*(adr_buf->adr_bus) == -1)
            {
                printf("WARNING: Adress Buffer attempt set adr with unassigned adr_bus\n");
            }
            adr_buf->adr = *(adr_buf->adr_bus);
            // printf("ADR Buff Load: " + str(adr_buf->adr));
        }
        if (*(adr_buf->we))
        {
            if (*(adr_buf->data_bus) == -1)
            {
                printf("WARNING: Adress Buffer attempt write to memory with unassigned data_bus\n");
            }
            // TODO: Fix this
            /*
            else if (adr_buf->adr >= CHAR_MEM_LOC and adr_buf->adr < CHAR_MEM_LOC + CHAR_MEM_SIZE):
                #print("char mem write")
                charMem[adr_buf->adr - CHAR_MEM_LOC] = adr_buf->data_bus
            else if (adr_buf->adr >= SCREEN_MEM_LOC and adr_buf->adr < SCREEN_MEM_LOC + SCREEN_MEM_SIZE):
                screenMem[adr_buf->adr - SCREEN_MEM_LOC] = adr_buf->data_bus
            else if (adr_buf->adr >= COLOR_MEM_LOC and adr_buf->adr < COLOR_MEM_LOC + COLOR_MEM_SIZE):
                colorMem[adr_buf->adr - COLOR_MEM_LOC] = adr_buf->data_bus
            else:
                try:
                */
            adr_buf->memory[adr_buf->adr] = *(adr_buf->data_bus);
            // except:
            //     print("ERROR: Attempt to write memory outside range.  ADR: " + hex(adr_buf->adr))
            // printf("Memory write - " + hex(adr_buf->adr) + ": " + hex(adr_buf->memory[adr_buf->adr]))
        }
    }
    adr_buf->prevclk = *(adr_buf->clk);

    if (*(adr_buf->ce))
    {
        // print("ADR Buff out adr: " + hex(adr_buf->adr))
        // print("ADR Buff out data: " + hex(adr_buf->memory[adr_buf->adr]))

        // TODO: Fix this
        /*
        if (adr_buf->adr >= CHAR_MEM_LOC and adr_buf->adr < CHAR_MEM_LOC + CHAR_MEM_SIZE):
            adr_buf->data_bus = charMem[adr_buf->adr - CHAR_MEM_LOC]
        elif (adr_buf->adr >= SCREEN_MEM_LOC and adr_buf->adr < SCREEN_MEM_LOC + SCREEN_MEM_SIZE):
            adr_buf->data_bus = screenMem[adr_buf->adr - SCREEN_MEM_LOC]
        elif (adr_buf->adr >= COLOR_MEM_LOC and adr_buf->adr < COLOR_MEM_LOC + COLOR_MEM_SIZE):
            adr_buf->data_bus = colorMem[adr_buf->adr - COLOR_MEM_LOC]
        else:
            if (adr_buf->adr_bus < RAM_SIZE_BYTES):
                try:
                */
        *(adr_buf->data_bus) = adr_buf->memory[adr_buf->adr];
        // except:
        //     print("ERROR: Attempt to write memory outside range.  ADR: " + hex(adr_buf->adr_bus))
    }
}