# OS Reference Guide

To run the emulated OS, use:

```sh
  python Compiler.py --os=goOSe.txt --disk=disk1.txt --run=True
  ```

| Parameter | Required/Optional | Default | Notes|
| --------- | ----------------- | ---- | ---- |
| os   |   Optional        | goOSe.txt | OS file to be compiled and run |
| disk    |   Optional        | [none] | Disk file to be attached.  Disk code starts at 0x5000 |
| run    |   Optional        | True | Run compiled code immediately after compiling if True. |

# Commands

## CLS

Syntax: CLS

Clears the screen.

## EXIT

Syntax: EXIT

Closes the OS.

## READ

Syntax: READ [address] [blocks]

Reads a specified number of 8-byte blocks from memory.

| Parameter | Required/Optional | Format | Notes|
| --------- | ----------------- | ---- | ---- |
| address   |   Required        | 2 bytes - hex | Starting address to read from.  Must be exactly 4 digits. |
| blocks    |   Optional        | 1 byte - hex | Number of 8-byte blocks to print.  Default is 1 if parameter not given. |

## WRITE

Syntax: WRITE [address] [data]

Writes 1 byte of data to a given address.

| Parameter | Required/Optional | Format | Notes|
| --------- | ----------------- | ---- | ---- |
| address   |   Required        | 2 bytes - hex |  Address to write to.  Must be exactly 4 digits. |
| data      |   Required        | 1 byte - hex |  Data to write to address. |

## RUN

Syntax: RUN [address]

Runs code starting at the given address.  To run disk.txt, use "RUN 5000".

| Parameter | Required/Optional | Format | Notes|
| --------- | ----------------- | ---- | ---- |
| address   |   Required        | 2 bytes - hex |  Address to run.  Must be exactly 4 digits. |
