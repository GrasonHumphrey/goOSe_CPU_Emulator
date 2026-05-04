#include <stdbool.h>

#ifndef address_buffer_h
#define address_buffer_h

struct address_buffer
{
    bool *ladd;
    bool *clk;
    bool *we;
    bool *ce;
    int *adr_bus;
    int *data_bus;
    bool *reset;

    int *memory;
    int adr;
    bool prevclk;
};

typedef struct address_buffer Address_Buffer;

void Load_Memory_From_File();

void Update_Address_Buffer(Address_Buffer *adr_buf);

#endif