import sys
import math
import time
from tkinter import *
from Graphics_Display import Graphics_Display
#import keyboard
from pynput.keyboard import Key, Listener

count = [False]
lip = [False]
lip1 = [False]
lip2 = [False]
clk = [False]
eip = [False]
eip_b = [False]
reset = [False]
adr_bus = [0]
ladd = [False]
we = [False]
ce = [False]
data_bus = [0]

linst = [False]
go = [False]

lt1 = [False]
lt2 = [False]
lta = [False]
et = [False]
et_b = [False]

lsp1 = [False]
lsp2 = [False]
lspa = [False]
esp = [False]
esp_b = [False]

lbp1 = [False]
lbp2 = [False]
lbpa = [False]
ebp = [False]
ebp_b = [False]

lrr1 = [False]
lrr2 = [False]
lrra = [False]
err = [False]
err_b = [False]

lacc = [False]
eacc = [False]
lbuff = [False]
ebuff = [False]
acc_alu_out = [0]
buff_alu_out = [0]

sel = [0]
cf = [False]
zf = [False]
sf = [False]
of = [False]
xf = [False]
clc = [False]
ealu = [False]


CHAR_MEM_SIZE = 0x1000
SCREEN_MEM_SIZE = 0x2000
COLOR_MEM_SIZE = 0x408
RAM_SIZE_BYTES = 0x1000
STACK_PTR_START = 0xDFF
KEY_BUF_BASE = 0xDE0
KEY_BUF_PTR_LOC = 0x0004

CODE_START_LOC = 0x100

charCodes = [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ',  '>', '_', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ":", '(', ')'],
             [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x20,0x3E,0x52,0x2E,0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39, 0x3A,0x28,0x29]]

charPressed = ''
charMem = [0 for i in range(CHAR_MEM_SIZE)]
screenMem = [0 for i in range(SCREEN_MEM_SIZE)]
colorMem = [0 for i in range(COLOR_MEM_SIZE)]

totalCycles = 0
systemHalt = False

ws = Tk()
ws.title('CPU Output')
#ws.geometry('300x300')
ws.config(bg='#000')

PIXEL_SCALE = 2
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

key_log = ""

canvas = Canvas(
    ws,
    height = SCREEN_HEIGHT,
    width = SCREEN_WIDTH,
    bg="#000"
)

canvas.pack()


class instruction_pointer:
    def __init__(self, count, lip, lip1, lip2, clk, eip, eip_b, reset, adr_bus, data_bus):
        self.count = count
        self.lip = lip
        self.lip1 = lip1
        self.lip2 = lip2
        self.clk = clk
        self.eip = eip
        self.eip_b = eip_b
        self.reset = reset
        self.adr_bus = adr_bus
        self.data_bus = data_bus
        self.adr = ['x']
        self.prevclk = [False]

    def Update(self):
        if (not self.prevclk[0]) and (self.clk[0]):
            if self.reset[0]:
                self.adr[0] = CODE_START_LOC
            if self.count[0]:
                self.adr[0] += 1
                #print("IP Count: " + hex(self.adr[0]))
            if self.lip[0]:
                if self.adr_bus[0] == 'x':
                    print("WARNING: Attempt load IP with unassigned adr_bus")
                self.adr[0] = self.adr_bus[0]
            if self.lip1[0]:
                if self.data_bus[0] == 'x':
                    print("WARNING: Attempt to load IP with unassigned data bus")
                self.adr[0] = (int(self.adr[0]) & 0xFF00) | int(data_bus[0])
                #print("LIP1: " + hex(data_bus[0]))
            if self.lip2[0]:
                if self.data_bus[0] == 'x':
                    print("WARNING: Attempt to load IP with unassigned data bus")
                self.adr[0] = (int(self.adr[0]) & 0x00FF) | (int(data_bus[0]) << 8)
                #print("LIP2: " + hex(data_bus[0]))
        self.prevclk[0] = self.clk[0]

        if self.eip[0]:
            if self.adr[0] == 'x':
                print("WARNING: IP attempt set adr_bus with unassigned adr")
            self.adr_bus[0] = self.adr[0]
            self.data_bus[0] = self.adr[0] & 0x00FF
        if self.eip_b[0]:
            self.adr_bus[0] = self.adr[0]
            self.data_bus[0] = (self.adr[0] & 0xFF00) >> 8

        self.prevclk[0] = self.clk[0]

class address_buffer:
    def __init__(self, ladd, clk, we, ce, adr_bus, data_bus, reset):
        self.ladd = ladd
        self.clk = clk
        self.we = we
        self.ce = ce
        self.adr_bus = adr_bus
        self.data_bus = data_bus
        self.reset = reset

        self.memory = [0 for i in range(RAM_SIZE_BYTES)]
        self.adr = ['x']
        self.prevclk = [False]

    def LoadMemoryFromFile(self):
        f = open("compiled_output.txt", "r")
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            self.memory[int(parts[0])] = int(parts[1], 16)

        # Set up key buffer memory
        self.memory[KEY_BUF_PTR_LOC] = (KEY_BUF_BASE+0x1F) & 0xFF
        #print("Init KEY_BUF_PTR_LOC: " + hex((KEY_BUF_BASE+0x1F) & 0xFF))
        self.memory[KEY_BUF_PTR_LOC+1] = ((KEY_BUF_BASE+0x1F) & 0xFF00) >> 8
        #print("Init KEY_BUF_PTR_LOC+1: " + hex(((KEY_BUF_BASE+0x1F) & 0xFF00) >> 8))

        #print(self.memory)


    def Update(self):
        # always @ posedge clk
        if (not self.prevclk[0]) and (self.clk[0]):
            if self.reset[0]:
                self.LoadMemoryFromFile()
                self.adr[0] = 0
            if self.ladd[0]:
                if self.adr_bus[0] == 'x':
                    print("WARNING: Adress Buffer attempt set adr with unassigned adr_bus")
                self.adr[0] = self.adr_bus[0]
                #print("ADR Buff Load: " + str(self.adr[0]))
            if self.we[0]:
                if self.data_bus[0] == 'x':
                    print("WARNING: Adress Buffer attempt write to memory with unassigned data_bus")
                if (self.adr[0] < RAM_SIZE_BYTES):
                    self.memory[self.adr[0]] = self.data_bus[0]
                elif (self.adr[0] < RAM_SIZE_BYTES + CHAR_MEM_SIZE):
                    print("char mem write")
                    charMem[self.adr[0] - RAM_SIZE_BYTES] = self.data_bus[0]
                elif (self.adr[0] < RAM_SIZE_BYTES + CHAR_MEM_SIZE + SCREEN_MEM_SIZE):
                    screenMem[self.adr[0] - RAM_SIZE_BYTES - CHAR_MEM_SIZE] = self.data_bus[0]
                elif (self.adr[0] < RAM_SIZE_BYTES + CHAR_MEM_SIZE + SCREEN_MEM_SIZE + COLOR_MEM_SIZE):
                    colorMem[self.adr[0] - RAM_SIZE_BYTES - CHAR_MEM_SIZE - SCREEN_MEM_SIZE] = self.data_bus[0]
                else:
                    print("ERROR: Attempt to write memory outside range.  ADR: " + hex(self.adr_bus[0]))
                #print("Memory write - " + hex(self.adr[0]) + ": " + hex(self.memory[self.adr[0]]))
        self.prevclk[0] = self.clk[0]
        # always @ *
        if self.ce[0]:
            #print("ADR Buff out adr: " + hex(self.adr[0]))
            #print("ADR Buff out data: " + hex(self.memory[self.adr[0]]))
            if (self.adr_bus[0] < RAM_SIZE_BYTES):
                self.data_bus[0] = self.memory[self.adr[0]]
            elif (self.adr_bus[0] < RAM_SIZE_BYTES + CHAR_MEM_SIZE):
                self.data_bus[0] = charMem[self.adr[0] - RAM_SIZE_BYTES]
            elif (self.adr_bus[0] < RAM_SIZE_BYTES + CHAR_MEM_SIZE + SCREEN_MEM_SIZE):
                self.data_bus[0] = screenMem[self.adr[0] - RAM_SIZE_BYTES - CHAR_MEM_SIZE]
            elif (self.adr_bus[0] < RAM_SIZE_BYTES + CHAR_MEM_SIZE + SCREEN_MEM_SIZE + COLOR_MEM_SIZE):
                self.data_bus[0] = colorMem[self.adr[0] - RAM_SIZE_BYTES - CHAR_MEM_SIZE - SCREEN_MEM_SIZE]
            else:
                print("ERROR: Attempt to write memory outside range.  ADR: " + hex(self.adr_bus[0]))



class ab_register:
    def __init__(self, lab, eab, clk, data_bus, alu_out):
        self.lab = lab
        self.eab = eab
        self.clk = clk
        self.data_bus = data_bus
        self.alu_out = alu_out
        self.data = [0]
        self.prevclk = [False]

    def Update(self):
        # always @ posedge clk
        if (not self.prevclk[0]) and (self.clk[0]):
            if self.lab[0]:
                if self.data_bus[0] == 'x':
                    print("WARNING: AB Reg attempt write to data with unassigned data_bus")
                self.data[0] = self.data_bus[0]
                #print("AB Load: " + str(self.data[0]))
        self.prevclk[0] = self.clk[0]
        # always @ *
        if self.eab[0]:
            self.data_bus[0] = self.data[0]
            #print("AB Out: " + str(self.data[0]))
        self.alu_out[0] = self.data[0]

class temporary_register:
    def __init__(self, lt1, lt2, lta, clk, et, et_b, data_bus, adr_bus):
        self.lt1 = lt1
        self.lt2 = lt2
        self.lta = lta
        self.clk = clk
        self.et = et
        self.et_b = et_b
        self.data_bus = data_bus
        self.adr_bus = adr_bus
        self.adr = [0]
        self.prevclk = [False]

    def Update(self):
        # always @ posedge clk
        if (not self.prevclk[0]) and (self.clk[0]):
            if self.lt1[0]:
                if self.data_bus[0] == 'x':
                    print("WARNING: Temp Reg attempt to load with unassigned data bus")
                self.adr[0] = (int(self.adr[0]) & 0xFF00) | int(data_bus[0])
                #print("TR Load: " + hex(self.adr[0]))
            if self.lt2[0]:
                if self.data_bus[0] == 'x':
                    print("WARNING: Temp Reg attempt to load with unassigned data bus")
                self.adr[0] = (int(self.adr[0]) & 0x00FF) | (int(data_bus[0]) << 8)
                #print("TR2 Load: " + hex(self.data_bus[0]))
            if self.lta[0]:
                if self.adr_bus[0] == 'x':
                    print("WARNING: Temp Reg attempt to load with unassigned adr bus")
                self.adr[0] = adr_bus[0]
        self.prevclk[0] = self.clk[0]
        # always @ *
        if self.et[0]:
            self.adr_bus[0] = self.adr[0]
            self.data_bus[0] = self.adr[0] & 0x00FF
            #print("TR Data Out: " + hex(self.adr[0] & 0x00FF))
            #print("TR Adr Out: " + hex(self.adr[0]))
        if self.et_b[0]:
            self.adr_bus[0] = self.adr[0]
            self.data_bus[0] = (self.adr[0] & 0xFF00) >> 8
            #print("TR Data Out: " + hex((self.adr[0] & 0xFF00) >> 8))

class arithmetic_logic_unit:
    def __init__(self, clk, data_bus, alu_in_a, alu_in_b, sel, ealu, cf, zf, sf, of, xf, clc):
        self.clk = clk
        self.data_bus = data_bus
        self.alu_in_a = alu_in_a
        self.alu_in_b = alu_in_b
        self.sel = sel
        self.ealu = ealu
        self.cf = cf
        self.zf = zf
        self.sf = sf
        self.of = of
        self.xf = xf
        self.clc = clc
        self.data = [0]

    def Update(self):
        # always @ *
        if self.clk[0]:
            overrideSF = False
            if self.clc[0]:
                self.cf[0] = False
                self.of[0] = False
                self.xf[0] = False
            if self.sel[0] == 0x0:
                # ADD
                result = (self.alu_in_a[0] + self.alu_in_b[0])
                    #print(hex(result)
                
                self.data[0] = result & 0xFF
                
                #print(self.alu_in_a[0])
                #print(self.alu_in_b[0])
                #print(self.data[0])
                #print()
                if self.ealu[0]:
                    #print("Add result: " + hex(result))
                    if self.cf[0]:
                        result += 1
                        self.data[0] = result & 0xFF
                        #print("carry")
                    #print("Add result: " + hex(self.data[0]))
                    # Calculate carry and overflow flags
                    # Set overflow flag if result is incorrect for signed arithmetic
                    #self.of[0] = (~(self.data[0]&0x80) and (self.alu_in_a[0]&0x80) and (self.alu_in_b[0]&0x80)) or ((self.data[0]&0x80) and ~(self.alu_in_a[0]&0x80) and ~(self.alu_in_b[0]&0x80))
                    self.of[0] = (result > 0x7F) or (result < -0x7F)
                    # Set carry flag if result is incorrect for unsigned arithmetic
                    #self.cf[0] = ((self.alu_in_a[0]&0x80) or (self.alu_in_b[0]&0x80)) and ~(self.data[0]&0x80)
                    self.cf[0] = result > 0xFF
                    #print(hex(result))
                    #print(self.cf[0])
                    # XF for carry needed with unsigned A and signed B
                    self.xf[0] = not ((self.alu_in_b[0] <= 0x7F and result <= 0xFF) or (self.alu_in_b[0] > 0x7F and result > 0xFF))
                    if self.xf[0]:
                        overrideSF = True
                        self.sf[0] = self.alu_in_b[0] > 0x7F

            if self.sel[0] == 0x1:
                # SUBTRACT
                result = (self.alu_in_a[0] - self.alu_in_b[0])
                self.data[0] = result & 0xFF
                if self.ealu[0]:
                    if self.cf[0]:
                        result -= 1
                        self.data[0] = result & 0xFF
                    #print("SUB AR: " + hex(self.alu_in_a[0]))
                    #print("SUB BR: " + hex(self.alu_in_b[0]))
                    #print("SUB Incoming CF: " + str(self.cf[0]))
                    #print("SUB result: " + hex(self.data[0]))
                    # Calculate carry and overflow flags
                    # Set overflow flag if result is incorrect for signed arithmetic
                    #self.of[0] = (~(self.data[0]&0x80) and (self.alu_in_a[0]&0x80) and (self.alu_in_b[0]&0x80)) or ((self.data[0]&0x80) and ~(self.alu_in_a[0]&0x80) and ~(self.alu_in_b[0]&0x80))
                    self.of[0] = (result > 0x7F) or (result < -0x7F)
                    # Set carry flag if result is incorrect for unsigned arithmetic
                    self.cf[0] = result < 0
                    # XF for carry needed with unsigned A and signed B
                    self.xf[0] = not ((self.alu_in_b[0] <= 0x7F and result <= 0xFF) or (self.alu_in_b[0] > 0x7F and result > 0xFF))
                    if self.xf[0]:
                        overrideSF = True
                        self.sf[0] = self.alu_in_b[0] > 0x7F
            if self.sel[0] == 0x2:
                # Bit shift left
                #result = (self.alu_in_a[0] << self.alu_in_b[0])
                result = (self.alu_in_a[0] << 1)
                self.data[0] = result & 0xFF
                self.cf[0] = result > 0xFF
            if self.sel[0] == 0x3:
                # Bit shift right
                #result = (self.alu_in_a[0] >> self.alu_in_b[0])
                result = (self.alu_in_a[0] >> 1)
                self.data[0] = result & 0xFF
                self.cf[0] = result < 0
            if self.sel[0] == 0x4:
                # Increment A
                result = self.alu_in_a[0] + 1
                self.data[0] = result & 0xFF
                if self.ealu[0]:
                    self.of[0] = (result > 0x7F) or (result < -0x7F)
                    self.cf[0] = result > 0xFF
            if self.sel[0] == 0x5:
                # Decrement A
                result = self.alu_in_a[0] - 1
                self.data[0] = result & 0xFF
                if self.ealu[0]:
                    self.of[0] = (result > 0x7F) or (result < -0x7F)
                    self.cf[0] = result < 0
            if self.sel[0] == 0x6:
                # Increment B
                result = self.alu_in_b[0] + 1
                self.data[0] = result & 0xFF
                if self.ealu[0]:
                    self.of[0] = (result > 0x7F) or (result < -0x7F)
                    self.cf[0] = result > 0xFF
            if self.sel[0] == 0x7:
                # Decrement B
                result = self.alu_in_b[0] - 1
                self.data[0] = result & 0xFF
                if self.ealu[0]:
                    self.of[0] = (result > 0x7F) or (result < -0x7F)
                    self.cf[0] = result < 0
            if self.sel[0] == 0x8:
                # AND A and B
                self.data[0] = self.alu_in_a[0] & self.alu_in_b[0]
            if self.sel[0] == 0x9:
                # OR A and B
                self.data[0] = self.alu_in_a[0] | self.alu_in_b[0]
            if self.sel[0] == 0xA:
                # XOR A and B
                self.data[0] = self.alu_in_a[0] ^ self.alu_in_b[0]
                #print("A: " + str(self.alu_in_a[0]))
                #print("B: " + str(self.alu_in_b[0]))
                #print("Data: " + str(self.data[0]))
            if self.sel[0] == 0xB:
                # NOT A
                self.data[0] = (~self.alu_in_a[0]) & 0xFF
            if self.sel[0] == 0xC:
                # NOT B
                self.data[0] = (~self.alu_in_b[0]) & 0xFF

            if self.ealu[0]:
                self.data_bus[0] = self.data[0]
                #print(self.data_bus[0])
                # Zero flag is set if result is zero
                self.zf[0] = self.data[0] == 0
                #print("ALU data: " + hex(self.data[0]))
                #print("ZF: " + str(self.zf[0]))
                #print
                # Sign flag is set if result is less than zero
                if not overrideSF:
                    self.sf[0] = self.data[0] & 0xFF > 0x7F
                    #print("EALU SF: " + str(self.sf[0]))

class instruction_register_control:
    def __init__(self, clk, data_bus, adr_bus, reset, go, eip, eip_b, ladd, ce, count, lt1, lt2, lta, we, lip, lip1, lip2, et, et_b, lsp1, lsp2, lspa, esp, esp_b, lbp1, lbp2, lbpa, ebp, ebp_b, lrr1, lrr2, lrra, err, err_b, lacc, eacc, lbuff, ebuff, sel, ealu, cf, zf, sf, of, xf, clc):
        self.clk = clk
        self.data_bus = data_bus
        self.adr_bus = adr_bus
        self.reset = reset
        self.go = go
        self.eip = eip
        self.eip_b = eip_b
        self.ladd = ladd
        self.ce = ce
        self.count = count
        self.lt1 = lt1
        self.lt2 = lt2
        self.lta = lta
        self.we = we
        self.lip = lip
        self.lip1 = lip1
        self.lip2 = lip2
        self.et = et
        self.et_b = et_b
        self.lsp1 = lsp1
        self.lsp2 = lsp2
        self.lspa = lspa
        self.esp = esp
        self.esp_b = esp_b
        self.lrr1 = lrr1
        self.lrr2 = lrr2
        self.lrra = lrra
        self.err = err
        self.err_b = err_b
        self.lbp1 = lbp1
        self.lbp2 = lbp2
        self.lbpa = lbpa
        self.ebp = ebp
        self.ebp_b = ebp_b
        self.lacc = lacc
        self.eacc = eacc
        self.lbuff = lbuff
        self.ebuff = ebuff
        self.sel = sel
        self.ealu = ealu
        self.cf = cf
        self.zf = zf
        self.sf = sf
        self.of = of
        self.xf = xf
        self.clc = clc
        self.linst = False
        self.data = [0]
        self.mema = False
        self.memb = False
        self.immeda = False
        self.immedb = False
        self.stora = False
        self.storb = False
        self.halt = False
        self.mov = False
        self.add = False
        self.sub = False
        self.log = False
        self.io = False
        self.swp = False
        self.shl = False
        self.shr = False
        self.deca = False
        self.decb = False
        self.inca = False
        self.incb = False
        self.aux = False
        self.jmp = False
        self.jz = False
        self.jnz = False
        self.jm = False
        self.jp = False
        self.jc = False
        self.jnc = False
        self.t = -1
        self.treset = False
        self.ff = False
        self.tf = False
        #self.execute = False
        self.prevclk = [False]
        self.shouldJump = False

    def ResetOutputs(self):
        self.eip[0] = False
        self.eip_b[0] = False
        self.ladd[0]  = False
        self.ce[0] = False
        self.lt1[0]  = False
        self.lt2[0] = False
        self.lta[0] = False
        self.we[0] = False
        self.count[0] = False
        self.lip[0] = False
        self.lip1[0] = False
        self.lip2[0] = False
        self.et[0] = False
        self.et_b[0] = False
        self.lacc[0] = False
        self.eacc[0] = False
        self.lbuff[0] = False
        self.ebuff[0] = False
        self.sel[0] = 0
        self.ealu[0] = False
        self.lrr1[0] = False
        self.lrr2[0] = False
        self.lrra[0] = False
        self.err[0] = False
        self.err_b[0] = False
        self.lsp1[0] = False
        self.lsp2[0] = False
        self.lspa[0] = False
        self.esp[0] = False
        self.esp_b[0] = False
        self.lbp1[0] = False
        self.lbp2[0] = False
        self.lbpa[0] = False
        self.ebp[0] = False
        self.ebp_b[0] = False
        self.clc[0] = False
        #self.data[0] = 0

    def ResetState(self):
        self.t = -1
        self.treset = False
        self.ff = False
        self.tf = False
        self.linst = False
        self.shouldJump = False
        #self.execute = False

    def ResetOpcodes(self):
        self.mema = False
        self.memb = False
        self.immeda = False
        self.immedb = False
        self.stora = False
        self.storb = False
        self.halt = False
        self.mov = False
        self.add = False
        self.sub = False
        self.log = False
        self.io = False
        self.swp = False
        self.shl = False
        self.shr = False
        self.inca = False
        self.incb = False
        self.aux = False
        self.deca = False
        self.decb = False
        self.jmp = False
        self.jz = False
        self.jnz = False
        self.jm = False
        self.jp = False
        self.jc = False
        self.jnc = False

    def SetOpcodes(self):
        lower = self.data[0] & 0x0F
        upper = (self.data[0] & 0xF0) >> 4
        global systemHalt
        #print(lower)
        #print(upper)

        if lower == 0x1:
            self.mema = True
        elif lower == 0x2:
            self.memb = True
        elif lower == 0x3:
            self.immeda = True
        elif lower == 0x4:
            self.immedb = True
        elif lower == 0x5:
            self.stora = True
        elif lower == 0x6:
            self.storb = True
        elif lower == 0x7:
            self.swp = True
        elif lower == 0x8:
            self.shl = True
        elif lower == 0x9:
            self.shr = True
        elif lower == 0xA:
            self.deca = True
        elif lower == 0xB:
            self.decb = True
        elif lower == 0xC:
            self.inca = True
        elif lower == 0xD:
            self.incb = True
        elif lower == 0xE:
            self.aux = True
        elif lower == 0xF:
            self.halt = True
            #global systemHalt
            systemHalt = True
            print("HALT received, exiting...")

        if upper == 0x0:
            self.mov = True
        elif upper == 0x1:
            self.add = True
        elif upper == 0x2:
            self.log = True
        elif upper == 0x3:
            self.io = True
        elif upper == 0x4:
            self.sub = True
        elif upper == 0x8:
            self.jmp = True
        elif upper == 0x9:
            self.jz = True
        elif upper == 0xA:
            self.jnz = True
        elif upper == 0xB:
            self.jm = True
        elif upper == 0xC:
            self.jp = True
        elif upper == 0xD:
            self.jc = True
        elif upper == 0xE:
            self.jnc = True
        elif upper == 0xF:
            self.halt = True
            #global systemHalt
            systemHalt = True
            #print("exiting...")

    def ZeroOperandOpcode(self):
        return (self.io or
                (self.add and self.immedb) or
                (self.sub and self.immedb) or
                (self.log and self.inca) or
                (self.log and self.incb) or
                (self.deca and self.log) or
                (self.decb and self.log) or
                (self.log and self.deca) or
                (self.mov and self.swp) or
                self.halt or
                (self.log and self.shl) or
                (self.log and self.shr) or
                (self.log and self.mema) or
                (self.log and self.memb) or
                (self.log and self.immeda) or
                (self.log and self.immedb) or
                (self.io and self.mema) or
                (self.io and self.memb) or
                (self.jmp and self.deca) or
                (self.jmp and self.aux) or
                (self.add and self.stora) or 
                (self.jmp and self.decb) or
                (self.mov and self.inca) or
                (self.jmp and self.inca) or
                (self.jmp and self.immedb) or
                (self.jz and self.immedb) or    # Jump to offset if zero
                (self.jnz and self.immedb) or   # Jump to offset if non-zero
                (self.jm and self.immedb) or    # Jump to offset if negative
                (self.jp and self.immedb) or    # Jump to offset if positive
                (self.jc and self.immedb) or    # Jump to offset if carry occurred
                (self.jnc and self.immedb) or   # Jump to offset if carry did not occur
                (self.jc and self.shl) or    # Jump to offset if carry occurred
                (self.jnc and self.shl) or
                (self.jmp and self.storb) or
                (self.jz and self.storb) or    
                (self.jnz and self.storb) or   
                (self.jm and self.storb) or    
                (self.jp and self.storb) or    
                (self.jc and self.storb) or    
                (self.jnc and self.storb) or   
                (self.jc and self.deca) or    
                (self.jnc and self.deca) or
                (self.jz and self.aux))

    def OneOperandOpcode(self):
        return ((self.mov and self.immeda) or   # Immediate move into A
                (self.mov and self.immedb) or   # Immediate move into B
                (self.mov and self.deca) or
                (self.mov and self.decb) or
                (self.add and self.immeda) or   # Immediately add
                (self.sub and self.immeda) or   # Immediately subtract
                (self.log and self.shr) or
                (self.log and self.shl) or      # Left and right bit shift
                (self.jmp and self.immeda) or
                (self.jz and self.immeda) or    # Jump to offset if zero
                (self.jnz and self.immeda) or   # Jump to offset if non-zero
                (self.jm and self.immeda) or    # Jump to offset if negative
                (self.jp and self.immeda) or    # Jump to offset if positive
                (self.jc and self.immeda) or    # Jump to offset if carry occurred
                (self.jnc and self.immeda) or   # Jump to offset if carry did not occur
                (self.jc and self.swp) or    # Jump to offset if overflow occurred
                (self.jnc and self.swp) or   # Jump to offset if overflow did not occur
                (self.jmp and self.stora) or
                (self.jz and self.stora) or    
                (self.jnz and self.stora) or   
                (self.jm and self.stora) or    
                (self.jp and self.stora) or    
                (self.jc and self.stora) or    
                (self.jnc and self.stora) or   
                (self.jc and self.shr) or    
                (self.jnc and self.shr) or
                (self.log and self.stora) or
                (self.log and self.storb) or
                (self.log and self.swp) or
                (self.jmp and self.shl) or
                (self.jmp and self.shr) or
                (self.jmp and self.swp))

    def Push(self, initTime):
        print("push")


    def Update(self):
        global buff
        global acc
        # always @ posedge clk
        if (not self.prevclk[0]) and (self.clk[0]):
            self.ResetOutputs()
            self.t += 1
            if self.linst:
                # Load new instruction
                self.ResetOpcodes()
                self.data[0] = self.data_bus[0]
                self.SetOpcodes()
            if self.reset[0] or self.treset or self.halt:
                # Reset IRC
                #print("IRC reset")
                self.ResetOutputs()
                self.ResetOpcodes()
                self.ResetState()

            # Opcode Fetch
            if self.ff == 0 and self.tf == 0:
                #print ("op fetch")
                if self.t == 0:
                    self.ResetOutputs()
                    self.eip[0] = True
                    self.ladd[0] = True
                    #print("****EIP load****")
                elif self.t == 1:
                    self.ce[0] = True
                    self.linst = True
                elif self.t == 2:
                    self.linst = False
                    self.count[0] = True
                    #print("Opcode: " + hex(self.data_bus[0]))
                    if self.ZeroOperandOpcode():
                        # Opcode with no operand, continue to execute
                        self.tf = True
                        #print("Zero operand opcode")
                    else:
                        # Fetch first operand for opcodes with 1 or more operands
                        self.t = -1
                        self.ff = True
                        #print("More than zero operand opcode")

            # First Operand Fetch
            elif self.ff:
                #print ("ff fetch")
                if self.t == 0:
                    self.ResetOutputs()
                    self.eip[0] = True
                    self.ladd[0] = True
                elif self.t == 1:
                    self.ce[0] = True
                    self.lt1[0] = True
                elif self.t == 2:
                    self.count[0] = True
                    self.tf = True
                    self.ff = False
                    if not self.OneOperandOpcode():
                        self.t = -1

            # Second Operand Fetch
            elif self.tf:
                #print ("tf fetch")
                #print("t: " + str(self.t))
                if self.t == 0:
                    self.ResetOutputs()
                    self.eip[0] = True
                    self.ladd[0] = True
                elif self.t == 1:
                    self.ce[0] = True
                    self.lt2[0] = True
                elif self.t == 2:
                    self.count[0] = True
                elif self.t >= 3:
                    # Execute

                    # MOV into A Immediate operation
                    if self.mov and self.immeda: 
                        #print ("mov")
                        if self.t == 3:
                            self.et[0] = True
                            self.lacc[0] = True
                        elif self.t == 4:
                            self.treset = True
                    
                    # MOV into B Immediate operation
                    elif self.mov and self.immedb:
                        if self.t == 3:
                            self.et[0] = True
                            self.lbuff[0] = True
                        elif self.t == 4:
                            #print("CF after MOV into B: " + str(self.cf[0]))
                            self.treset = True
                    
                    # MOV A into MEM                        
                    elif self.mov and self.stora:
                        if self.t == 3:
                            self.et[0] = True
                            self.ladd[0] = True
                            #print("here")
                        elif self.t == 4:
                            self.eacc[0] = True
                            self.we[0] = True
                        elif self.t == 5:
                            self.treset = True
                    
                    # MOV B into MEM
                    elif self.mov and self.storb:
                        if self.t == 3:
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            self.ebuff[0] = True
                            #print("Enable B")
                            #print("Count: " + str(self.count[0]))
                            self.we[0] = True
                        elif self.t == 5:
                            self.treset = True
                    
                    # MOV MEM into A
                    elif self.mov and self.mema:
                        #print("MOV MEM into A")
                        if self.t == 3:
                            #print("Set LADD")
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            #print("Clear LADD")
                            self.ce[0] = True
                            self.lacc[0] = True
                        elif self.t == 5:
                            self.treset = True
                            #global totalCycles
                            #print("Finish MOV MEM into A")
                    
                    # MOV MEM into B
                    elif self.mov and self.memb:
                        if self.t == 3:
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            self.ce[0] = True
                            self.lbuff[0] = True
                        elif self.t == 5:
                            self.treset = True

                    # STO: Store A into offset at B from given address in MEM                        
                    elif self.mov and self.shr:
                        if self.t == 3:
                            # Save A
                            self.lrr1[0] = True
                            self.eacc[0] = True
                        elif self.t == 4:
                            # Load lower byte of address into A
                            self.et[0] = True
                            self.lacc[0] = True
                        elif self.t == 5:
                            # Add A and B
                            self.lacc[0] = True
                            self.ealu[0] = True
                            self.sel[0] = 0
                        elif self.t == 6:
                            # Move result to temp1
                            #print("A+B: " + hex(self.data_bus[0]))
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 7:
                            # Load high byte of address into A
                            self.lacc[0] = True
                            self.et_b[0] = True
                        elif self.t == 8:
                            # Decide if upper byte of BP needs to be incremented
                            #print("BP_B: " + hex(self.data_bus[0]))
                            if self.xf[0]:
                                self.lacc[0] = True
                                self.ealu[0] = True
                                if self.sf[0]:
                                    # Offset was negative, decrement A
                                    self.sel[0] = 5
                                else:
                                    # Offset was positive, increment A
                                    self.sel[0] = 4
                        elif self.t == 9:
                            # Move result to temp2
                            self.eacc[0] = True
                            self.lt2[0] = True
                        elif self.t == 10:
                            # Move temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 11:
                            # Write saved value of A and restore A
                            #print("Address: " + hex(self.adr_bus[0]))
                            self.err[0] = True
                            self.we[0] = True
                            self.lacc[0] = True
                            self.clc[0] = True
                        elif self.t == 12:
                            # Call finished
                            self.treset = True
                            #print("finish STO")

                    # LDO: Load into A from offset at B from given address in MEM                        
                    elif self.mov and self.shl:
                        if self.t == 3:
                            # Load lower byte of address into A
                            self.et[0] = True
                            self.lacc[0] = True
                        elif self.t == 4:
                            # Add A and B
                            self.lacc[0] = True
                            self.ealu[0] = True
                            self.sel[0] = 0
                        elif self.t == 5:
                            # Move result to temp1
                            #print("A+B: " + hex(self.data_bus[0]))
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 6:
                            # Load high byte of address into A
                            self.lacc[0] = True
                            self.et_b[0] = True
                        elif self.t == 7:
                            # Decide if upper byte of BP needs to be incremented
                            #print("BP_B: " + hex(self.data_bus[0]))
                            if self.xf[0]:
                                self.lacc[0] = True
                                self.ealu[0] = True
                                if self.sf[0]:
                                    # Offset was negative, decrement A
                                    self.sel[0] = 5
                                else:
                                    # Offset was positive, increment A
                                    self.sel[0] = 4
                        elif self.t == 8:
                            # Move result to temp2
                            self.eacc[0] = True
                            self.lt2[0] = True
                        elif self.t == 9:
                            # Move temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 10:
                            # Read into A from MEM
                            #print("Address: " + hex(self.adr_bus[0]))
                            self.ce[0] = True
                            self.lacc[0] = True
                            self.clc[0] = True
                        elif self.t == 11:
                            # Call finished
                            self.treset = True
                            #print("finish poke")

                    # STZ <immed>: Store A into offset at B from given zero-page pointer address              
                    elif self.mov and self.decb:
                        if self.t == 3:
                            # Save A to RR1
                            self.eacc[0] = True
                            self.lrr1[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                            # Load 0 into T2
                            self.lt2[0] = True
                            self.data_bus[0] = 0x0
                        elif self.t == 5:
                            # Load temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 6:
                            # Read from MEM into A
                            self.ce[0] = True
                            self.lacc[0] = True
                        elif self.t == 7:
                            # Add offset in B to A, then save to RR2
                            self.ealu[0] = True
                            self.lrr2[0] = True
                            self.sel[0] = 0
                        elif self.t == 8:
                            # Load lower byte of address to A from T1
                            self.et[0] = True
                            self.lacc[0] = True
                        elif self.t == 9:
                            # Increment lower byte of address
                            self.ealu[0] = True
                            self.lt1[0] = True
                            self.sel[0] = 4
                        elif self.t == 10:
                            # Load incremented temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 11:
                            # Read from MEM into T2
                            self.ce[0] = True
                            self.lt2[0] = True
                        elif self.t == 12:
                            # Move saved address in RR2 to T1
                            self.err_b[0] = True
                            self.lt1[0] = True
                        elif self.t == 13:
                            # Load address in temp reg to address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 14:
                            # Write stored A in RR1 to MEM and restore A
                            self.err[0] = True
                            self.we[0] = True
                            self.clc[0] = True
                            self.lacc[0] = True
                        elif self.t == 15:
                            # Finish STZ
                            self.treset = True

                    # LDZ <immed>: Load A from offset at B from given zero-page pointer address              
                    elif self.mov and self.deca:
                        if self.t == 3:
                            # Load 0 into T2
                            self.clc[0] = True
                            self.lt2[0] = True
                            self.data_bus[0] = 0x0
                        elif self.t == 4:
                            # Load temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 5:
                            # Read from MEM into A
                            self.ce[0] = True
                            self.lacc[0] = True
                        elif self.t == 6:
                            # Add offset in B to A, then save to RR2
                            self.ealu[0] = True
                            self.lrr2[0] = True
                            self.sel[0] = 0
                        elif self.t == 7:
                            # Load lower byte of address to A from T1
                            self.et[0] = True
                            self.lacc[0] = True
                        elif self.t == 8:
                            # Increment lower byte of address
                            self.ealu[0] = True
                            self.lt1[0] = True
                            self.sel[0] = 4
                        elif self.t == 9:
                            # Load incremented temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 10:
                            # Read from MEM into T2
                            self.ce[0] = True
                            self.lt2[0] = True
                        elif self.t == 11:
                            # Move saved address in RR2 to T1
                            self.err_b[0] = True
                            self.lt1[0] = True
                        elif self.t == 12:
                            # Load address in temp reg to address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 13:
                            # Read MEM into A
                            self.lacc[0] = True
                            self.ce[0] = True
                            self.clc[0] = True
                        elif self.t == 14:
                            # Finish LDZ
                            self.treset = True

                    # LDZ Ar: Load A from offset at B from Ar zero-page pointer address              
                    elif self.mov and self.inca:
                        if self.t == 3:
                            # Load 0 into T2
                            self.clc[0] = True
                            self.lt2[0] = True
                            self.data_bus[0] = 0x0
                        elif self.t == 4:
                            # Load Ar into T1
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 5:
                            # Load temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 6:
                            # Read from MEM into A
                            self.ce[0] = True
                            self.lacc[0] = True
                        elif self.t == 7:
                            # Add offset in B to A, then save to RR2
                            self.ealu[0] = True
                            self.lrr2[0] = True
                            self.sel[0] = 0
                        elif self.t == 8:
                            # Load lower byte of address to A from T1
                            self.et[0] = True
                            self.lacc[0] = True
                        elif self.t == 9:
                            # Increment lower byte of address
                            self.ealu[0] = True
                            self.lt1[0] = True
                            self.sel[0] = 4
                        elif self.t == 10:
                            # Load incremented temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 11:
                            # Read from MEM into T2
                            self.ce[0] = True
                            self.lt2[0] = True
                        elif self.t == 12:
                            # Move saved address in RR2 to T1
                            self.err_b[0] = True
                            self.lt1[0] = True
                        elif self.t == 13:
                            # Load address in temp reg to address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 14:
                            # Read MEM into A
                            #print("LDZ from address: " + hex(self.adr_bus[0]))
                            self.lacc[0] = True
                            self.ce[0] = True
                            self.clc[0] = True
                        elif self.t == 15:
                            # Finish LDZ
                            self.treset = True

                    # ADD Immediate
                    elif self.add and self.immeda:
                        if self.t == 3:
                            # Save B reg
                            self.ebuff[0] = True
                            self.lrr1[0] = True
                        elif self.t == 4:
                            self.et[0] = True
                            self.lbuff[0] = True
                        elif self.t == 5:
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 0
                        elif self.t == 6:
                            # Restore B reg
                            self.lbuff[0] = True
                            self.err[0] = True
                            self.sel[0] = 0
                        elif self.t == 7:
                            self.treset = True
                            #print("Finish ADD Immediate")
                    
                    # ADD MEM
                    elif self.add and self.mema:
                        if self.t == 3:
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            self.ce[0] = True
                            self.lbuff[0] = True
                        elif self.t == 5:
                            self.treset = True
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 0
                    
                    # ADD B to A
                    elif self.add and self.immedb:
                        if self.t == 3:
                            self.ealu[0] = True
                            self.lacc[0] = True
                            #print("Add t=3")
                            self.sel[0] = 0
                            #print(self.data_bus)
                        elif self.t == 4:
                            self.treset = True
                    
                    # Clear carry flag
                    elif self.add and self.stora:
                        if self.t == 3:
                            self.clc[0] = True
                            #print(self.data_bus)
                        elif self.t == 4:
                            self.treset = True

                    # SUB Immediate
                    elif self.sub and self.immeda:
                        if self.t == 3:
                            # Save B reg
                            self.ebuff[0] = True
                            self.lrr1[0] = True
                        elif self.t == 4:
                            self.et[0] = True
                            self.lbuff[0] = True
                        elif self.t == 5:
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 1
                        elif self.t == 6:
                            # Restore B reg
                            self.lbuff[0] = True
                            self.err[0] = True
                            self.sel[0] = 0
                        elif self.t == 7:
                            self.treset = True
                            #print("Finish SUB immediate")
                    
                    # SUB MEM
                    elif self.sub and self.mema:
                        #print("sub mem")
                        if self.t == 3:
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            self.ce[0] = True
                            self.lbuff[0] = True
                        elif self.t == 5:
                            self.treset = True
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 1
                    
                    # SUB B from A
                    elif self.sub and self.immedb:
                        #print("Sub A-B")
                        if self.t == 3:
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 1
                        elif self.t == 4:
                            #print("CF after sub: " + str(self.cf[0]))
                            self.treset = True

                    # Swap A and B
                    elif self.swp and self.mov:
                        if self.t == 3:
                            #print("Start SWP")
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 4:
                            self.ebuff[0] = True
                            self.lacc[0] = True
                        elif self.t == 5:
                            self.lbuff[0] = True
                            self.et[0] = True
                        elif self.t == 6:
                            self.treset = True
                            #print("Finish swap")

                    # Jump to memory address
                    elif ((self.jmp and self.mema) or 
                          (self.jz and self.mema) or 
                          (self.jnz and self.mema) or
                          (self.jm and self.mema) or
                          (self.jp and self.mema) or
                          (self.jc and self.mema) or
                          (self.jnc and self.mema) or
                          (self.jc and self.memb) or
                          (self.jnc and self.memb)):
                        if self.t == 3:
                            if ((self.jmp and self.mema) or 
                                (self.jz and self.mema and self.zf[0]) or 
                                (self.jnz and self.mema and not self.zf[0]) or
                                (self.jm and self.mema and self.sf[0]) or
                                (self.jp and self.mema and not self.sf[0]) or
                                (self.jc and self.mema and self.cf[0]) or
                                (self.jnc and self.mema and not self.cf[0]) or
                                (self.jc and self.memb and self.of[0]) or
                                (self.jnc and self.memb and not self.of[0])):
                                self.et[0] = True
                                self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
       
                    # Jump to immediate offset
                    elif ((self.jmp and self.immeda) or 
                          (self.jz and self.immeda) or
                          (self.jnz and self.immeda) or
                          (self.jm and self.immeda) or
                          (self.jp and self.immeda) or
                          (self.jc and self.immeda) or
                          (self.jnc and self.immeda) or
                          (self.jc and self.swp) or
                          (self.jnc and self.swp)):
                        if self.t == 3:
                            # Save A
                            self.eacc[0] = True
                            self.lrr1[0] = True
                        elif self.t == 4:
                            # Save B
                            self.ebuff[0] = True
                            self.lrr2[0] = True
                        elif self.t == 5:
                            # Load offset into B
                            self.et[0] = True
                            self.lbuff[0] = True
                        elif self.t == 6:
                            # Load instruction pointer low byte into A
                            self.eip[0] = True
                            self.lacc[0] = True
                        elif self.t == 7:
                            # Add A and B and save to temp
                            if ((self.jmp and self.immeda) or 
                                (self.jz and self.immeda and self.zf[0]) or 
                                (self.jnz and self.immeda and not self.zf[0]) or
                                (self.jm and self.immeda and self.sf[0]) or
                                (self.jp and self.immeda and not self.sf[0]) or
                                (self.jc and self.immeda and self.cf[0]) or
                                (self.jnc and self.immeda and not self.cf[0]) or
                                (self.jc and self.swp and self.of[0]) or
                                (self.jnc and self.swp and not self.of[0])):
                                self.clc[0] = True
                                self.ealu[0] = True
                                self.lt1[0] = True
                                self.sel[0] = 0
                            else:
                                # Just load old IP into temp to avoid jump
                                self.clc[0] = True
                                self.lt1[0] = True
                                self.eip[0] = True
                        elif self.t == 8:
                            # Load high byte of IP into A and temp
                            self.lacc[0] = True
                            self.lt2[0] = True
                            self.eip_b[0] = True
                        elif self.t == 9:
                            # Increment high byte of IP if carry
                            if self.xf[0]:
                                #print("Carry")
                                self.lt2[0] = True
                                self.ealu[0] = True
                                if self.sf[0]:
                                    # Offset was negative, decrement A
                                    self.sel[0] = 5
                                else:
                                    # Offset was positive, increment A
                                    self.sel[0] = 4
                        elif self.t == 10:
                            # Set IP to new offset IP
                            self.lip[0] = True
                            self.et[0] = True
                        elif self.t == 11:
                            # Restore A
                            self.lacc[0] = True
                            self.err[0] = True
                        elif self.t == 12:
                            # Restore B
                            self.lbuff[0] = True
                            self.err_b[0] = True
                        elif self.t == 13:
                            self.treset = True
                    
                    # Jump to Ar offset
                    elif ((self.jmp and self.immedb) or 
                          (self.jz and self.immedb) or
                          (self.jnz and self.immedb) or
                          (self.jm and self.immedb) or
                          (self.jp and self.immedb) or
                          (self.jc and self.immedb) or
                          (self.jnc and self.immedb) or
                          (self.jc and self.shl) or
                          (self.jnc and self.shl)):
                        if self.t == 3:
                            # Save A
                            self.eacc[0] = True
                            self.lrr1[0] = True
                        elif self.t == 4:
                            # Save B
                            self.ebuff[0] = True
                            self.lrr2[0] = True
                        elif self.t == 5:
                            # Load instruction pointer low byte into B
                            self.eip[0] = True
                            self.lbuff[0] = True
                        elif self.t == 6:
                            # Add A and B and save to temp
                            if ((self.jmp and self.immedb) or 
                                (self.jz and self.immedb and self.zf[0]) or 
                                (self.jnz and self.immedb and not self.zf[0]) or
                                (self.jm and self.immedb and self.sf[0]) or
                                (self.jp and self.immedb and not self.sf[0]) or
                                (self.jc and self.immedb and self.cf[0]) or
                                (self.jnc and self.immedb and not self.cf[0]) or
                                (self.jc and self.shl and self.of[0]) or
                                (self.jnc and self.shl and not self.of[0])):
                                self.ealu[0] = True
                                self.lt1[0] = True
                                self.clc[0] = True
                                self.sel[0] = 0
                            else:
                                # Just load old IP into temp to avoid jump
                                self.clc[0] = True
                                self.lt1[0] = True
                                self.eip[0] = True
                        elif self.t == 7:
                            # Load high byte of IP into A and temp
                            self.lacc[0] = True
                            self.lt2[0] = True
                            self.eip_b[0] = True
                        elif self.t == 8:
                            # Increment high byte of IP if carry
                            if self.xf[0]:
                                #print("Carry")
                                self.lt2[0] = True
                                self.ealu[0] = True
                                if self.sf[0]:
                                    # Offset was negative, decrement A
                                    self.sel[0] = 5
                                else:
                                    # Offset was positive, increment A
                                    self.sel[0] = 4
                        elif self.t == 9:
                            # Set IP to new offset IP
                            self.lip[0] = True
                            self.et[0] = True
                        elif self.t == 10:
                            # Restore A
                            self.lacc[0] = True
                            self.err[0] = True
                        elif self.t == 11:
                            # Restore B
                            self.lbuff[0] = True
                            self.err_b[0] = True
                        elif self.t == 12:
                            self.treset = True

                    # Jump to immediate zero-page address
                    elif ((self.jmp and self.stora) or 
                          (self.jz and self.stora) or
                          (self.jnz and self.stora) or
                          (self.jm and self.stora) or
                          (self.jp and self.stora) or
                          (self.jc and self.stora) or
                          (self.jnc and self.stora) or
                          (self.jc and self.shr) or
                          (self.jnc and self.shr)):
                        if self.t == 3:
                            if ((self.jmp and self.stora) or 
                                (self.jz and self.stora and self.zf[0]) or 
                                (self.jnz and self.stora and not self.zf[0]) or
                                (self.jm and self.stora and self.sf[0]) or
                                (self.jp and self.stora and not self.sf[0]) or
                                (self.jc and self.stora and self.cf[0]) or
                                (self.jnc and self.stora and not self.cf[0]) or
                                (self.jc and self.shr and self.of[0]) or
                                (self.jnc and self.shr and not self.of[0])):
                                    self.shouldJump = True
                            # Save A
                            self.eacc[0] = True
                            self.lrr1[0] = True
                        elif self.t == 4:
                            # Save B
                            self.ebuff[0] = True
                            self.lrr2[0] = True
                        elif self.t == 5:
                            # Load 0 into T2
                            self.clc[0] = True
                            self.lt2[0] = True
                            self.data_bus[0] = 0x0
                        elif self.t == 6:
                            # Load temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 7:
                            # Read from MEM into B
                            self.ce[0] = True
                            self.lbuff[0] = True
                        elif self.t == 8:
                            # Load lower byte of address to A from T1
                            self.et[0] = True
                            self.lacc[0] = True
                        elif self.t == 9:
                            # Increment lower byte of address
                            self.clc[0] = True
                            self.ealu[0] = True
                            self.lt1[0] = True
                            self.sel[0] = 4
                        elif self.t == 10:
                            # Load incremented temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 11:
                            # Read from MEM into T2
                            self.ce[0] = True
                            self.lt2[0] = True
                        elif self.t == 12:
                            # Move saved address in B to T1
                            self.ebuff[0] = True
                            self.lt1[0] = True
                        elif self.t == 13:
                            # Load address in temp reg to address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 14:
                            # Load new IP from memory
                            if (self.shouldJump):
                                self.lip[0] = True
                                self.ce[0] = True
                        elif self.t == 15:
                            # Restore A
                            self.lacc[0] = True
                            self.err[0] = True
                        elif self.t == 16:
                            # Restore B
                            self.lbuff[0] = True
                            self.err_b[0] = True
                        elif self.t == 17:
                            self.treset = True
                    
                    # Jump to zero-page address in Ar
                    elif ((self.jmp and self.storb) or 
                          (self.jz and self.storb) or
                          (self.jnz and self.storb) or
                          (self.jm and self.storb) or
                          (self.jp and self.storb) or
                          (self.jc and self.storb) or
                          (self.jnc and self.storb) or
                          (self.jc and self.deca) or
                          (self.jnc and self.deca)):
                        if self.t == 3:
                            if ((self.jmp and self.storb) or 
                                (self.jz and self.storb and self.zf[0]) or 
                                (self.jnz and self.storb and not self.zf[0]) or
                                (self.jm and self.storb and self.sf[0]) or
                                (self.jp and self.storb and not self.sf[0]) or
                                (self.jc and self.storb and self.cf[0]) or
                                (self.jnc and self.storb and not self.cf[0]) or
                                (self.jc and self.deca and self.of[0]) or
                                (self.jnc and self.deca and not self.of[0])):
                                    self.shouldJump = True
                            # Save A and load A into T1
                            self.eacc[0] = True
                            self.lrr1[0] = True
                            self.lt1[0] = True
                        elif self.t == 4:
                            # Save B
                            self.ebuff[0] = True
                            self.lrr2[0] = True
                        elif self.t == 5:
                            # Load 0 into T2
                            self.clc[0] = True
                            self.lt2[0] = True
                            self.data_bus[0] = 0x0
                        elif self.t == 6:
                            # Load temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 7:
                            # Read from MEM into B
                            self.ce[0] = True
                            self.lbuff[0] = True
                        elif self.t == 8:
                            # Load lower byte of address to A from RR1
                            self.err[0] = True
                            self.lacc[0] = True
                        elif self.t == 9:
                            # Increment lower byte of address
                            self.ealu[0] = True
                            self.lt1[0] = True
                            self.clc[0] = True
                            self.sel[0] = 4
                        elif self.t == 10:
                            # Load incremented temp into address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 11:
                            # Read from MEM into T2
                            self.ce[0] = True
                            self.lt2[0] = True
                        elif self.t == 12:
                            # Move saved address in B to T1
                            self.ebuff[0] = True
                            self.lt1[0] = True
                        elif self.t == 13:
                            # Load address in temp reg to address reg
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 14:
                            # Load new IP from memory
                            if (self.shouldJump):
                                self.lip[0] = True
                                self.ce[0] = True
                        elif self.t == 15:
                            # Restore A
                            self.lacc[0] = True
                            self.err[0] = True
                        elif self.t == 16:
                            # Restore B
                            self.lbuff[0] = True
                            self.err_b[0] = True
                        elif self.t == 17:
                            self.treset = True
                    
                    
                    # No operand ALU operations
                    elif ((self.log and self.shl) or
                          (self.log and self.shr) or
                          (self.log and self.inca) or
                          (self.log and self.incb) or
                          (self.log and self.deca) or
                          (self.log and self.decb) or
                          (self.log and self.mema) or
                          (self.log and self.memb) or
                          (self.log and self.immeda) or
                          (self.log and self.immedb)):
                        if self.t == 3:
                            self.ealu[0] = True
                            self.lacc[0] = True
                            if self.log and self.shl:
                                # Left shift
                                self.sel[0] = 2
                            elif self.log and self.shr:
                                # Right shift
                                self.sel[0] = 3
                            elif self.log and self.inca:
                                # Increment A
                                self.sel[0] = 4
                            elif self.log and self.deca:
                                # Decrement A
                                self.sel[0] = 5
                            elif self.log and self.incb:
                                # Increment B
                                self.sel[0] = 6
                                self.lacc[0] = False
                                self.lbuff[0] = True
                            elif self.log and self.decb:
                                # Decrement B
                                self.sel[0] = 7
                                self.lacc[0] = False
                                self.lbuff[0] = True
                            elif self.log and self.mema:
                                # AND A and B
                                self.sel[0] = 8
                            elif self.log and self.memb:
                                # OR A and B
                                self.sel[0] = 9
                            elif self.log and self.immeda:
                                # XOR A and B
                                self.sel[0] = 0xA
                            elif self.log and self.immedb:
                                # NOT A
                                self.sel[0] = 0xB
                        elif self.t == 4:
                            self.treset = True
                    
                    
                    # One operand ALU operations
                    elif ((self.log and self.stora) or
                          (self.log and self.storb) or
                          (self.log and self.swp)):
                        if self.t == 3:
                        # Save B reg
                            self.ebuff[0] = True
                            self.lrr1[0] = True
                        elif self.t == 4:
                            self.et[0] = True
                            self.lbuff[0] = True
                        elif self.t == 5:
                            self.ealu[0] = True
                            self.lacc[0] = True
                            if self.log and self.stora:
                                # AND immed
                                self.sel[0] = 8
                            elif self.log and self.storb:
                                # OR immed
                                self.sel[0] = 9
                            elif self.log and self.swp:
                                # XOR immed
                                self.sel[0] = 0xA
                        elif self.t == 6:
                            # Restore B reg
                            self.lbuff[0] = True
                            self.err[0] = True
                            self.sel[0] = 0
                        elif self.t == 7:
                            self.treset = True
                    
                    # IO A
                    elif self.io and self.mema:
                        if self.t == 3:
                            self.treset = True
                            print("Clock cycles: " + str(totalCycles))
                            print("A REG: " + str(format(acc.data[0], '#x')))
                    
                    # IO B
                    elif self.io and self.memb:
                        if self.t == 3:
                            self.treset = True
                            print("Clock cycles: " + str(totalCycles))
                            print("B REG: " + str(format(buff.data[0], '#x')))

                    # CALL Function
                    elif self.jz and self.incb:
                        if self.t == 3:
                            # Save A
                            self.lrr1[0] = True
                            self.eacc[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                            # Save B
                            self.lrr2[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            ## Load low byte of stack pointer into A
                            self.lacc[0] = True
                            self.esp[0] = True
                        elif self.t == 6:
                            # Load high byte of stack pointer into B
                            self.esp_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 7:
                            # Increment lower byte of stack pointer in A
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 8:
                            # Increment upper byte of stack pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 9:
                            # Load new SP into address register
                            self.ladd[0] = True
                            self.esp[0] = True
                            self.clc[0] = True
                        elif self.t == 10:
                            # Write lower byte of IP to stack
                            self.we[0] = True
                            self.eip[0] = True
                        elif self.t == 11:
                            # Increment lower byte of stack pointer in A
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 12:
                            # Increment upper byte of stack pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 13:
                            # Load new SP into address register
                            self.ladd[0] = True
                            self.esp[0] = True
                            self.clc[0] = True
                        elif self.t == 14:
                            # Write upper byte of IP to stack
                            self.we[0] = True
                            self.eip_b[0] = True
                        elif self.t == 15:
                            # Increment lower byte of stack pointer in A
                            
                            #print(hex(self.data_bus[0]))
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 16:
                            # Increment upper byte of stack pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 17:
                            # Load new SP into address register
                            self.ladd[0] = True
                            self.esp[0] = True
                            self.clc[0] = True
                        elif self.t == 18:
                            # Save lower byte of BP to stack
                            self.we[0] = True
                            self.ebp[0] = True
                        elif self.t == 19:
                            # Increment lower byte of stack pointer in A
                            #print("CALL saved lower BP: " + hex(self.data_bus[0]))
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 20:
                            # Increment upper byte of stack pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 21:
                            # Load new SP into address register
                            self.ladd[0] = True
                            self.esp[0] = True
                            self.clc[0] = True
                        elif self.t == 22:
                            # Save upper byte of BP to stack
                            #print("CALL set new SP: " + hex(self.adr_bus[0]))
                            self.we[0] = True
                            self.ebp_b[0] = True
                        elif self.t == 23:
                            # Set BP to SP
                            #print("CALL saved upper BP: " + hex(self.data_bus[0]))
                            self.lbpa[0] = True
                            self.esp[0] = True
                        elif self.t == 24:
                            # Set IP to be call address
                            #print("CALL set new BP: " + hex(self.adr_bus[0]))
                            self.lip[0] = True
                            self.et[0] = True
                        elif self.t == 25:
                            # Restore A
                            self.err[0] = True
                            self.lacc[0] = True
                        elif self.t == 26:
                            # Restore B
                            self.err_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 27:
                            # Call finished
                            self.treset = True

                    # Return from Function
                    elif self.jz and self.aux:
                        if self.t == 3:
                            # Save A
                            self.lrr1[0] = True
                            self.eacc[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                            # Save B
                            #print ("Saved A: " + hex(self.data_bus[0]))
                            self.lrr2[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            ## Load low byte of base pointer into A
                            #print ("Saved B: " + hex(self.data_bus[0]))
                            self.lacc[0] = True
                            self.ebp[0] = True
                        elif self.t == 6:
                            # Load high byte of base pointer into B
                            self.ebp_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 7:
                            # Load BP into address register
                            self.ladd[0] = True
                            self.ebp[0] = True
                        elif self.t == 8:
                            # Load upper byte of BP from stack into T2
                            self.ce[0] = True
                            self.lt2[0] = True
                            #print ("SP into ADR: " + hex(self.adr_bus[0]))
                        elif self.t == 9:
                            # Decrement lower byte of base pointer in A
                            #print("RET restored upper BP: " + hex(self.data_bus[0]))
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lbp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 10:
                            # Decrement upper byte of base pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lbp2[0] = True
                                self.sel[0] = 7
                        elif self.t == 11:
                            # Load BP into address register
                            self.ladd[0] = True
                            self.ebp[0] = True
                        elif self.t == 12:
                            # Load lower byte of BP from stack into T1
                            self.ce[0] = True
                            self.lt1[0] = True
                        elif self.t == 13:
                            # Decrement lower byte of base pointer in A
                            #print("RET restored lower BP: " + hex(self.data_bus[0]))
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lbp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 14:
                            # Decrement upper byte of stack pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lbp2[0] = True
                                self.sel[0] = 7
                        elif self.t == 15:
                            # Load BP into address register
                            self.ladd[0] = True
                            self.ebp[0] = True
                        elif self.t == 16:
                            # Load upper byte of IP from stack
                            self.ce[0] = True
                            self.lip2[0] = True
                        elif self.t == 17:
                            # Decrement lower byte of base pointer in A
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lbp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 18:
                            # Decrement upper byte of stack pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lbp2[0] = True
                                self.sel[0] = 7
                        elif self.t == 19:
                            # Load BP into address register
                            self.ladd[0] = True
                            self.ebp[0] = True
                        elif self.t == 20:
                            # Load lower byte of IP from stack
                            self.ce[0] = True
                            self.lip1[0] = True
                        elif self.t == 21:
                            # Decrement lower byte of base pointer in A
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lbp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 22:
                            # Decrement upper byte of base pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lbp2[0] = True
                                self.sel[0] = 7
                        elif self.t == 23:
                            # Set SP to decremented BP
                            self.ebp[0] = True
                            self.lspa[0] = True
                        elif self.t == 24:
                            # Set BP to new saved BP in T
                            self.et[0] = True
                            self.lbpa[0] = True
                        elif self.t == 25:
                            # Restore A
                            #print("RET restored BP: " + hex(self.adr_bus[0]))
                            self.err[0] = True
                            self.lacc[0] = True
                            self.clc[0] = True
                        elif self.t == 26:
                            # Restore B
                            #print ("Restored A: " + hex(self.data_bus[0]))
                            self.err_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 27:
                            # Call finished
                            #print ("Restored B: " + hex(self.data_bus[0]))
                            self.treset = True

                    # Peek at <immed> BP offset
                    elif self.jmp and self.shl:
                        if self.t == 3:
                         # Save B
                            self.lrr1[0] = True
                            self.ebuff[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                            # Load low byte of base pointer into A
                            self.lacc[0] = True
                            self.ebp[0] = True
                        elif self.t == 5:
                            # Load offset into B
                            self.lbuff[0] = True
                            self.et[0] = True
                        elif self.t == 6:
                            # Add A and B
                            self.lacc[0] = True
                            self.ealu[0] = True
                            self.sel[0] = 0
                        elif self.t == 7:
                            # Move result to temp1
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 8:
                            # Load BP2 into A
                            self.ebp_b[0] = True
                            self.lacc[0] = True
                        elif self.t == 9:
                            # Decide if upper byte of BP needs to be incremented
                            #print("BP_B: " + hex(self.data_bus[0]))
                            if self.xf[0]:
                                #print("Carry")
                                self.lacc[0] = True
                                self.ealu[0] = True
                                if self.sf[0]:
                                    # Offset was negative, decrement A
                                    self.sel[0] = 5
                                else:
                                    # Offset was positive, increment A
                                    self.sel[0] = 4
                        elif self.t == 10:
                            # Move result to temp2
                            self.eacc[0] = True
                            self.lt2[0] = True
                        elif self.t == 11:
                            # Move temp into address reg
                            #print("ACC: " + hex(self.data_bus[0]))
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 12:
                            # Move output into A
                            self.lacc[0] = True
                            self.ce[0] = True
                        elif self.t == 13:
                            # Restore B
                            self.err[0] = True
                            self.lbuff[0] = True
                            self.clc[0] = True
                        elif self.t == 14:
                            # Call finished
                            self.clc[0] = False
                            self.treset = True
                    
                    # Peek at B reg BP offset
                    elif self.jmp and self.aux:
                        #print("A reg peek")
                        if self.t == 3:
                            # Save A
                            self.lrr1[0] = True
                            self.eacc[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                         # Save B
                            self.lrr2[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            # Load low byte of base pointer into A
                            self.lacc[0] = True
                            self.ebp[0] = True
                        elif self.t == 6:
                            # Load offset into B
                            self.lbuff[0] = True
                            self.err_b[0] = True
                        elif self.t == 7:
                            # Add A and B
                            #print("Offset: " + hex(self.data_bus[0]))
                            self.lacc[0] = True
                            self.ealu[0] = True
                            self.sel[0] = 0
                        elif self.t == 8:
                            # Move result to temp1
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 9:
                            # Load BP2 into A
                            self.ebp_b[0] = True
                            self.lacc[0] = True
                        elif self.t == 10:
                            # Decide if upper byte of BP needs to be incremented
                            #print("BP_B: " + hex(self.data_bus[0]))
                            if self.xf[0]:
                                #print("Carry")
                                self.lacc[0] = True
                                self.ealu[0] = True
                                if self.sf[0]:
                                    # Offset was negative, decrement A
                                    self.sel[0] = 5
                                else:
                                    # Offset was positive, increment A
                                    self.sel[0] = 4
                        elif self.t == 11:
                            # Move result to temp2
                            self.eacc[0] = True
                            self.lt2[0] = True
                        elif self.t == 12:
                            # Move temp into address reg
                            #print("ACC: " + hex(self.data_bus[0]))
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 13:
                            # Move output into A
                            self.lacc[0] = True
                            self.ce[0] = True
                        elif self.t == 14:
                            # Restore B
                            self.err_b[0] = True
                            self.lbuff[0] = True
                            self.clc[0] = True
                        elif self.t == 15:
                            # Call finished
                            self.treset = True
                            
                    # Poke A to <immed> BP offset
                    elif self.jmp and self.shr:
                        if self.t == 3:
                         # Save A to RR2
                            self.eacc[0] = True
                            self.lrr2[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                         # Save B to RR1
                            #print("Saved A: " + hex(self.data_bus[0]))
                            self.lrr1[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            # Load low byte of base pointer into A
                            self.lacc[0] = True
                            self.ebp[0] = True
                        elif self.t == 6:
                            # Load offset into B
                            self.lbuff[0] = True
                            self.et[0] = True
                        elif self.t == 7:
                            # Add A and B
                            self.lacc[0] = True
                            self.ealu[0] = True
                            self.sel[0] = 0
                        elif self.t == 8:
                            # Move result to temp1
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 9:
                            # Load BP2 into A
                            self.ebp_b[0] = True
                            self.lacc[0] = True
                        elif self.t == 10:
                            # Decide if upper byte of BP needs to be incremented
                            #print("BP_B: " + hex(self.data_bus[0]))
                            if self.xf[0]:
                                #print("Carry")
                                self.lacc[0] = True
                                self.ealu[0] = True
                                if self.sf[0]:
                                    # Offset was negative, decrement A
                                    self.sel[0] = 5
                                else:
                                    # Offset was positive, increment A
                                    self.sel[0] = 4
                        elif self.t == 11:
                            # Move result to temp2
                            self.eacc[0] = True
                            self.lt2[0] = True
                        elif self.t == 12:
                            # Move temp into address reg
                            #print("ACC: " + hex(self.data_bus[0]))
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 13:
                            # Write saved value of A and restore A
                            self.err_b[0] = True
                            self.we[0] = True
                            self.lacc[0] = True
                        elif self.t == 14:
                            # Restore B
                            #print("Saved A: " + hex(self.data_bus[0]))
                            self.err[0] = True
                            self.lbuff[0] = True
                            self.clc[0] = True
                        elif self.t == 15:
                            # Call finished
                            self.treset = True
                            #print("finish poke")

                    # Poke A to B reg BP offset
                    elif self.jmp and self.inca:
                        if self.t == 3:
                         # Save A to RR2
                            self.eacc[0] = True
                            self.lrr2[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                         # Save B to RR1
                            #print("Saved A: " + hex(self.data_bus[0]))
                            self.lrr1[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            # Load low byte of base pointer into A
                            self.lacc[0] = True
                            self.ebp[0] = True
                        elif self.t == 6:
                            # Add A and B
                            self.lacc[0] = True
                            self.ealu[0] = True
                            self.sel[0] = 0
                        elif self.t == 7:
                            # Move result to temp1
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 8:
                            # Load BP2 into A
                            self.ebp_b[0] = True
                            self.lacc[0] = True
                        elif self.t == 9:
                            # Decide if upper byte of BP needs to be incremented
                            #print("BP_B: " + hex(self.data_bus[0]))
                            if self.xf[0]:
                                #print("Carry")
                                self.lacc[0] = True
                                self.ealu[0] = True
                                if self.sf[0]:
                                    # Offset was negative, decrement A
                                    self.sel[0] = 5
                                else:
                                    # Offset was positive, increment A
                                    self.sel[0] = 4
                        elif self.t == 10:
                            # Move result to temp2
                            self.eacc[0] = True
                            self.lt2[0] = True
                        elif self.t == 11:
                            # Move temp into address reg
                            #print("ACC: " + hex(self.data_bus[0]))
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 12:
                            # Write saved value of A and restore A
                            self.err_b[0] = True
                            self.we[0] = True
                            self.lacc[0] = True
                        elif self.t == 13:
                            # Call finished
                            self.treset = True
                            #print("finish poke")

                    # Pop from SP
                    elif self.jmp and self.deca:
                        if self.t == 3:
                         # Save B
                            self.lrr1[0] = True
                            self.ebuff[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                            # Load stack pointer into address reg and A
                            self.lacc[0] = True
                            self.esp[0] = True
                            self.ladd[0] = True
                        elif self.t == 5:
                            # Move output into RR2
                            self.lrr2[0] = True
                            self.ce[0] = True
                        elif self.t == 6:
                            # Load high byte of stack pointer into B
                            self.esp_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 7:
                            # Decrement lower byte of stack pointer in A
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 8:
                            # Decrement upper byte of stack pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 7
                        elif self.t == 9:
                            # Move saved value from RR2 to A
                            self.err_b[0] = True
                            self.lacc[0] = True
                        elif self.t == 10:
                            # Restore B
                            self.err[0] = True
                            self.lbuff[0] = True
                            self.clc[0] = True
                        elif self.t == 11:
                            # Pop finished
                            self.treset = True

                    # Push A reg to SP
                    elif self.jmp and self.decb:
                        if self.t == 3:
                         # Save A
                            self.lrr1[0] = True
                            self.eacc[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                         # Save B
                            self.lrr2[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            # Load stack pointer lower byte into A
                            self.lacc[0] = True
                            self.esp[0] = True
                        elif self.t == 6:
                            # Load high byte of stack pointer into B
                            self.esp_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 7:
                            # Increment lower byte of stack pointer in A
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 8:
                            # Increment upper byte of stack pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 9:
                            # Load stack pointer into address register
                            self.ladd[0] = True
                            self.esp[0] = True
                        elif self.t == 10:
                            # Write saved A in RR1 to SP and restore A
                            self.err[0] = True
                            self.we[0] = True
                            self.lacc[0] = True
                        elif self.t == 11:
                            # Restore B
                            self.err_b[0] = True
                            self.lbuff[0] = True
                            self.clc[0] = True
                        elif self.t == 12:
                            # Push finished
                            self.treset = True
                            #print("Finish reg push")

                    # Push <immed> to SP
                    elif self.jmp and self.swp:
                        if self.t == 3:
                         # Save A
                            self.lrr1[0] = True
                            self.eacc[0] = True
                            self.clc[0] = True
                        elif self.t == 4:
                         # Save B
                            self.lrr2[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            # Load stack pointer lower byte into A
                            self.lacc[0] = True
                            self.esp[0] = True
                        elif self.t == 6:
                            # Load high byte of stack pointer into B
                            self.esp_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 7:
                            # Increment lower byte of stack pointer in A
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 8:
                            # Increment upper byte of stack pointer in B if carry
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 9:
                            # Load stack pointer into address register
                            self.ladd[0] = True
                            self.esp[0] = True
                        elif self.t == 10:
                            # Write <immed> to SP
                            self.et[0] = True
                            self.we[0] = True
                        elif self.t == 11:
                            # Restore A
                            self.err[0] = True
                            self.lacc[0] = True
                            self.clc[0] = True
                        elif self.t == 12:
                            # Restore B
                            self.err_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 13:
                            # Push finished
                            self.treset = True

        self.prevclk[0] = self.clk[0]

        # always @ *
        #self.SetOpcodes()




ip = instruction_pointer(count, lip, lip1, lip2, clk, eip, eip_b, reset, adr_bus, data_bus)
ab = address_buffer(ladd, clk, we, ce, adr_bus, data_bus, reset)
tr = temporary_register(lt1, lt2, lta, clk, et, et_b, data_bus, adr_bus)
rr = temporary_register(lrr1, lrr2, lrra, clk, err, err_b, data_bus, adr_bus)
sp = temporary_register(lsp1, lsp2, lspa, clk, esp, esp_b, data_bus, adr_bus)
bp = temporary_register(lbp1, lbp2, lbpa, clk, ebp, ebp_b, data_bus, adr_bus)
alu = arithmetic_logic_unit(clk, data_bus, acc_alu_out, buff_alu_out, sel, ealu, cf, zf, sf, of, xf, clc)
acc = ab_register(lacc, eacc, clk, data_bus, acc_alu_out)
buff = ab_register(lbuff, ebuff, clk, data_bus, buff_alu_out)
irc = instruction_register_control(clk, data_bus, adr_bus, reset, go, eip, eip_b, ladd, ce, count, lt1, lt2, lta, we, lip, lip1, lip2, et, et_b, lsp1, lsp2, lspa, esp, esp_b, lbp1, lbp2, lbpa, ebp, ebp_b, lrr1, lrr2, lrra, err, err_b, lacc, eacc, lbuff, ebuff, sel, ealu, cf, zf, sf, of, xf, clc)

display = Graphics_Display(charMem, screenMem, colorMem, 0, canvas, SCREEN_WIDTH, SCREEN_HEIGHT, PIXEL_SCALE)

screenFocus = True

def key_handler(key: Key):
    global key_log
    if(screenFocus):
    #if(True):
        try:
            if (key.char in charCodes[0]):
                key_log += key.char
                charCode = charCodes[1][charCodes[0].index(key.char)]
                #print(hex(charCode))
                # Keyboard inputs go in a 32-byte ring buffer
                ab.memory[KEY_BUF_PTR_LOC] = ((ab.memory[KEY_BUF_PTR_LOC] + 1) & 0x1F) | (KEY_BUF_BASE & 0xFF)
                keyBufLoc = ab.memory[KEY_BUF_PTR_LOC] + (ab.memory[KEY_BUF_PTR_LOC+1] << 8)
                #print(hex(keyBufLoc))
                ab.memory[keyBufLoc] = charCode
        except AttributeError:
            if (key == key.enter):
                #print("Enter")
                key_log += '\n'
                with open("key_log.txt", "a") as file:
                    file.write(key_log)
                    file.close()
                key_log = ""
                ab.memory[KEY_BUF_PTR_LOC] = ((ab.memory[KEY_BUF_PTR_LOC] + 1) & 0x1F) | (KEY_BUF_BASE & 0xFF)
                keyBufLoc = ab.memory[KEY_BUF_PTR_LOC] + (ab.memory[KEY_BUF_PTR_LOC+1] << 8)
                #print(hex(keyBufLoc))
                ab.memory[keyBufLoc] = 0x00
            elif (key == key.backspace):
                #print("Backspace")
                if (len(key_log) > 0):
                    key_log = key_log[:-1]
                keyBufLoc = ab.memory[KEY_BUF_PTR_LOC] + (ab.memory[KEY_BUF_PTR_LOC+1] << 8)
                # Don't backspace past line return
                if (not ab.memory[keyBufLoc] == 0):
                    ab.memory[KEY_BUF_PTR_LOC] = ((ab.memory[KEY_BUF_PTR_LOC] + 1) & 0x1F) | (KEY_BUF_BASE & 0xFF)
                    keyBufLoc = ab.memory[KEY_BUF_PTR_LOC] + (ab.memory[KEY_BUF_PTR_LOC+1] << 8)
                    #print(hex(keyBufLoc))
                    ab.memory[keyBufLoc] = 0x1F
                    ab.memory[KEY_BUF_PTR_LOC] = ((ab.memory[KEY_BUF_PTR_LOC] - 2) & 0x1F) | (KEY_BUF_BASE & 0xFF)
            elif (key == key.space):
                #print("Space")
                key_log += " "
                ab.memory[KEY_BUF_PTR_LOC] = ((ab.memory[KEY_BUF_PTR_LOC] + 1) & 0x1F) | (KEY_BUF_BASE & 0xFF)
                keyBufLoc = ab.memory[KEY_BUF_PTR_LOC] + (ab.memory[KEY_BUF_PTR_LOC+1] << 8)
                #print(hex(keyBufLoc))
                ab.memory[keyBufLoc] = 0x20
            

listener = Listener(on_press=key_handler)
listener.start()

sp.adr[0] = STACK_PTR_START
bp.adr[0] = STACK_PTR_START

def Update_All():
    #adr_bus[0] = 'x'
    #data_bus[0] = 'x'
    alu.Update()
    ip.Update()
    ab.Update()
    tr.Update()
    acc.Update()
    buff.Update()
    sp.Update()
    bp.Update()
    rr.Update()
    irc.Update()
    #adr_bus[0] = 'x'
    #data_bus[0] = 'x'

def Toggle_Clk():
    clk[0] = False
    Update_All()
    clk[0] = True
    Update_All()
    clk[0] = False

def Toggle_Reset():
    reset[0] = True
    Toggle_Clk()
    reset[0] = False

def dbgprint(output):
    print(format(output, '#x'))

def Print_Final_Dump():
    print()
    print("***** Final Output Dump *****")
    print("Clock cycles: " + str(totalCycles))
    print("A REG: " + str(format(acc.data[0], '#x')))
    print("B REG: " + str(format(buff.data[0], '#x')))

def Dump_Memory():
    with open("memory_dump.txt", "w") as file:
        i = 0
        numZeros = int(math.log10(RAM_SIZE_BYTES)) + 2
        file.write("       0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\n")
        while i < RAM_SIZE_BYTES:
            file.write(f"{i:#0{numZeros}x}" + ": ")
            for j in range(16):
                file.write(f"{ab.memory[i+j]:02x}" + " ")

            file.write("\n")
            i += 16
        file.close()



def TestBench1():
    Toggle_Reset()
    count[0] = True
    Toggle_Clk()
    Toggle_Clk()
    count[0] = False
    eip[0] = True
    ladd[0] = True
    Toggle_Clk()
    dbgprint(adr_bus[0])

    eip[0] = False
    ladd[0] = False
    ce[0] = True
    lt2[0] = True
    Toggle_Clk()
    ce[0] = False
    lt2[0] = False
    et_b[0] = True
    Toggle_Clk()
    dbgprint(data_bus[0])

def TestBench2():
    startTime = time.time_ns()
    #print("Start time: " + str(startTime))
    Toggle_Reset()
    global totalCycles
    global screenFocus

    with open("key_log.txt", "w") as file:
        file.write("")
        file.close()

    #while (totalCycles < 100000) and not systemHalt:
    while not systemHalt:
        totalCycles += 1
        Toggle_Clk()
        if (totalCycles % 5000 == 0):
            totalCycles = 1
            display.update()
            #key_handler()
            #print(focus)
            ws.update()
            screenFocus = ws.focus_get()
            Dump_Memory()

    endTime = time.time_ns()
    #print("End time: " + str(endTime))
    deltaTime = endTime - startTime
    #print("ns taken: " + str(deltaTime))
    #print("Real clock rate: " + str(1000000000*totalCycles/deltaTime))

    display.update()
    Print_Final_Dump()
    Dump_Memory()
    ws.destroy()

TestBench2()