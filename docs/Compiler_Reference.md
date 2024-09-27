# Compiler Reference Guide

## Instruction Set

### MOV [Ar/Br] [MEM]

- Description: Move value at memory into A or B.
- Opcode: MOV && MEMA/MEMB (0x01/0x02)
- Clock cycles: 12
- Memory bytes: 3

### MOV [Ar/Br] <immed>

- Description: Move immediate value into A or B.
- Opcode: MOV && IMMEDA/IMMEDB (0x03/0x04)
- Clock cycles: 8
- Memory bytes: 2

### MOV [MEM] [Ar/Br]

- Description: Move value in A or B into memory.
- Opcode: MOV && STORA/STORB (0x05/0x06)
- Clock cycles: 12
- Memory bytes: 3

### SWP

- Description: Swap A and B registers.
- Opcode: SWP && MOV (0x07)
- Clock cycles: 7
- Memory bytes: 1

### LDO [MEM]

- Description: Load into A from given address in MEM with offset in B.
- Opcode: MOV && SHL (0x08)
- Clock cycles: 18
- Memory bytes: 3

### STO [MEM]

- Description: Store A into given address in MEM with offset in B.
- Opcode: MOV && SHR (0x09)
- Clock cycles: 19
- Memory bytes: 3

### LDZ Ar

- Description: Load into A from zero-page pointer address in A with offset in B.
- Opcode: MOV && INCA (0x0C)
- Clock cycles: 16
- Memory bytes: 1

### LDZ [$ZP]

- Description: Load into A from given zero-page pointer address with offset in B.
- Opcode: MOV && DECA (0x0A)
- Clock cycles: 18
- Memory bytes: 2

### STZ [$ZP]

- Description: Store A into given zero-page pointer address with offset in B.
- Opcode: MOV && DECB (0x0B)
- Clock cycles: 19
- Memory bytes: 2

### PUSH Ar

- Description: Push A onto the stack and increment the stack pointer.
- Opcode: JMP && DECB (0x8B)
- Clock cycles: 13
- Memory bytes: 1

### PUSH <immed>

- Description: Push the given value onto the stack and increment the stack pointer.
- Opcode: JMP && SWP (0x87)
- Clock cycles: 17
- Memory bytes: 2

### POP

- Description: Pop from the stack into A and decrement the stack pointer.
- Opcode: JMP && DECA (0x8A)
- Clock cycles: 12
- Memory bytes: 1

### PEEK Br

- Description: Load into A from the base pointer with the offset in B.
- Opcode: JMP && AUX (0x8E)
- Clock cycles: 16
- Memory bytes: 1

### PEEK <immed>

- Description: Load into A from the base pointer with the given offset.
- Opcode: JMP && AUX (0x88)
- Clock cycles: 18
- Memory bytes: 2

### POKE Br

- Description: Store A into base pointer with the offset in B.
- Opcode: JMP && INCA (0x8C)
- Clock cycles: 14
- Memory bytes: 1

### POKE <immed>

- Description: Store A into base pointer with the given offset.
- Opcode: JMP && SHR (0x89)
- Clock cycles: 19
- Memory bytes: 2

### CALL [MEM]

- Description: Call a function at given memory location.  Set new stack pointer and base pointer appropriately.
- Opcode: JMP && STORA (0x85)
- Clock cycles: 34
- Memory bytes: 3

### RET

- Description: Return from a function.  Set new stack pointer and base pointer appropriately.
- Opcode: JMP && STORB (0x86)
- Clock cycles: 28
- Memory bytes: 1

### SHL

- Description: Bit shift left A register 1 bit
- Opcode: LOG && SHL (0x28)
- Clock cycles: 5
- Memory bytes: 1

### SHR

- Description: Bit shift right A register 1 bit
- Opcode: LOG && SHR (0x29)
- Clock cycles: 5
- Memory bytes: 1

### INC [Ar/Br]

- Description: Increment A/B register
- Opcode: LOG && INCA/INCB (0x2C/0x2D)
- Clock cycles: 5
- Memory bytes: 1

### DEC [Ar/Br]

- Description: Decrement A/B register
- Opcode: LOG && DECA/DECB (0x2A/0x2B)
- Clock cycles: 5
- Memory bytes: 1

### AND Br

- Description: Bitwise AND A and B register
- Opcode: LOG && MEMA (0x21)
- Clock cycles: 5
- Memory bytes: 1

### AND <immed>

- Description: Bitwise AND immediate value with A
- Opcode: LOG && STORA (0x25)
- Clock cycles: 11
- Memory bytes: 2

### OR Br

- Description: Bitwise OR A and B register
- Opcode: LOG && MEMB (0x22)
- Clock cycles: 5
- Memory bytes: 1

### OR <immed>

- Description: Bitwise OR immediate value with A
- Opcode: LOG && STORB (0x26)
- Clock cycles: 11
- Memory bytes: 2

### XOR Br

- Description: Bitwise XOR A and B register
- Opcode: LOG && IMMEDA (0x23)
- Clock cycles: 5
- Memory bytes: 1

### XOR <immed>

- Description: Bitwise XOR immediate value with A
- Opcode: LOG && SWP (0x27)
- Clock cycles: 11
- Memory bytes: 2

### NOT

- Description: Bitwise NOT A register
- Opcode: LOG && IMMEDB (0x24)
- Clock cycles: 5
- Memory bytes: 1

### IO [Ar/Br]

- Description: Print value of A/B register to console
- Opcode: IO && MEMA/MEMB (0x31/0x32)
- Clock cycles: 4
- Memory bytes: 1