# OS Reference Guide

# Commands

## CLS

Syntax: CLS

Clears the screen.

## EXIT

Syntax: EXIT

Closes the OS.

## READ

Syntax: READ [address] [blocks]

| Parameter | Required/Optional | Format | Notes|
| --------- | ----------------- | ---- | ---- |
| address   |   Required        | 2 bytes - hex | Starting address to read from.  Must be exactly 4 digits. |
| blocks    |   Optional        | 1 byte - hex | Number of 8-byte blocks to print.  Default is 1 if parameter not given. |

## WRITE

Syntax: WRITE [address] [data]

| Parameter | Required/Optional | Format | Notes|
| --------- | ----------------- | ---- | ---- |
| address   |   Required        | 2 bytes - hex |  Address to write to.  Must be exactly 4 digits. |
| data      |   Required        | 1 byte - hex |  Data to write to address. |