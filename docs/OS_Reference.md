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

| Parameter | Required/Optional | Notes|
| --------- | ----------------- | ---- |
| address   |   Required        | Starting address to read from.  Must be exactly 4 digits. |
| blocks    |   Optional        | Number of 8-byte blocks to print.  Default is 1 if parameter not given. |

## WRITE

Syntax: WRITE [address] [data]

| Parameter | Required/Optional | Notes|
| --------- | ----------------- | ---- |
| address   |   Required        | Address to write to.  Must be exactly 4 digits. |
| data      |   Required        | Data to write to address. |