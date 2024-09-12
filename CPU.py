import sys
import math
import time
from tkinter import *
from Graphics_Display import Graphics_Display

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
ealu = [False]


CHAR_MEM_SIZE = 0x1000
SCREEN_MEM_SIZE = 0x2000
RAM_SIZE_BYTES = 0x1000
STACK_PTR_START = 0xE00

charMem = [0 for i in range(CHAR_MEM_SIZE)]
screenMem = [0 for i in range(SCREEN_MEM_SIZE)]

totalCycles = 0
systemHalt = False

ws = Tk()
ws.title('CPU Output')
#ws.geometry('300x300')
ws.config(bg='#000')

PIXEL_SCALE = 2
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

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
                self.adr[0] = 0
            if self.count[0]:
                self.adr[0] += 1
                #print("IP Count: " + str(self.adr[0]))
            if self.lip[0]:
                if self.adr_bus[0] == 'x':
                    print("WARNING: Attempt load IP with unassigned adr_bus")
                self.adr[0] = self.adr_bus[0]
            if self.lip1[0]:
                if self.data_bus[0] == 'x':
                    print("WARNING: Attempt to load IP with unassigned data bus")
                self.adr[0] = (int(self.adr[0]) & 0xFF00) | int(data_bus[0])
            if self.lip2[0]:
                if self.data_bus[0] == 'x':
                    print("WARNING: Attempt to load IP with unassigned data bus")
                self.adr[0] = (int(self.adr[0]) & 0x00FF) | (int(data_bus[0]) << 8)
        self.prevclk[0] = self.clk[0]

        if self.eip[0]:
            if self.adr[0] == 'x':
                print("WARNING: IP attempt set adr_bus with unassigned adr")
            self.adr_bus[0] = self.adr[0]
            self.data_bus[0] = self.adr[0] & 0x00FF
        if self.eip_b[0]:
            self.adr_bus[0] = self.adr[0]
            self.data_bus[0] = self.adr[0] & 0xFF00

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
                if (self.adr_bus[0] < RAM_SIZE_BYTES):
                    self.memory[self.adr[0]] = self.data_bus[0]
                elif (self.adr_bus[0] < RAM_SIZE_BYTES + CHAR_MEM_SIZE):
                    charMem[self.adr[0] - RAM_SIZE_BYTES] = self.data_bus[0]
                elif (self.adr_bus[0] < RAM_SIZE_BYTES + CHAR_MEM_SIZE + SCREEN_MEM_SIZE):
                    screenMem[self.adr[0] - RAM_SIZE_BYTES - CHAR_MEM_SIZE] = self.data_bus[0]
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
                print("TR2 Load: " + hex(self.data_bus[0]))
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
    def __init__(self, clk, data_bus, alu_in_a, alu_in_b, sel, ealu, cf, zf, sf, of, xf):
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
        self.data = [0]

    def Update(self):
        # always @ *
        overrideSF = False
        if self.sel[0] == 0x0:
            # ADD
            result = (self.alu_in_a[0] + self.alu_in_b[0])
            self.data[0] = result & 0xFF
            
            #print(self.alu_in_a[0])
            #print(self.alu_in_b[0])
            #print(self.data[0])
            #print()
            if self.ealu[0]:
                #print("Add result: " + hex(self.data[0]))
                # Calculate carry and overflow flags
                # Set overflow flag if result is incorrect for signed arithmetic
                #self.of[0] = (~(self.data[0]&0x80) and (self.alu_in_a[0]&0x80) and (self.alu_in_b[0]&0x80)) or ((self.data[0]&0x80) and ~(self.alu_in_a[0]&0x80) and ~(self.alu_in_b[0]&0x80))
                self.of[0] = (result > 0x7F) or (result < -0x7F)
                # Set carry flag if result is incorrect for unsigned arithmetic
                #self.cf[0] = ((self.alu_in_a[0]&0x80) or (self.alu_in_b[0]&0x80)) and ~(self.data[0]&0x80)
                self.cf[0] = result > 0xFF
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
            # Sign flag is set if result is less than zero
            if not overrideSF:
                self.sf[0] = self.data[0] & 0xFF > 0x7F

class instruction_register_control:
    def __init__(self, clk, data_bus, adr_bus, reset, go, eip, eip_b, ladd, ce, count, lt1, lt2, lta, we, lip, lip1, lip2, et, et_b, lsp1, lsp2, lspa, esp, esp_b, lbp1, lbp2, lbpa, ebp, ebp_b, lrr1, lrr2, lrra, err, err_b, lacc, eacc, lbuff, ebuff, sel, ealu, cf, zf, sf, of, xf):
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
        self.t = 0
        self.treset = False
        self.ff = False
        self.tf = False
        #self.execute = False
        self.prevclk = [False]

    def ResetOutputs(self):
        self.eip[0] = False
        self.ladd[0]  = False
        self.ce[0] = False
        self.lt1[0]  = False
        self.lt2[0] = False
        self.lta[0] = False
        self.we[0] = False
        self.count[0] = False
        self.lip[0] = False
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
        self.data[0] = 0

    def ResetState(self):
        self.t = 0
        self.treset = False
        self.ff = False
        self.tf = False
        self.linst = False
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
                (self.jmp and self.storb) or
                (self.jmp and self.deca) or
                (self.jmp and self.aux))

    def OneOperandOpcode(self):
        return ((self.mov and self.immeda) or   # Immediate move into A
                (self.mov and self.immedb) or   # Immediate move into B
                (self.add and self.immeda) or   # Immediately add
                (self.sub and self.immeda) or   # Immediately subtract
                (self.log and self.shr) or
                (self.log and self.shl) or      # Left and right bit shift
                (self.jz and self.immeda) or    # Jump to offset if zero
                (self.jnz and self.immeda) or   # Jump to offset if non-zero
                (self.jm and self.immeda) or    # Jump to offset if negative
                (self.jp and self.immeda) or    # Jump to offset if positive
                (self.jc and self.immeda) or    # Jump to offset if carry occurred
                (self.jnc and self.immeda) or   # Jump to offset if carry did not occur
                (self.jc and self.immedb) or    # Jump to offset if overflow occurred
                (self.jnc and self.immedb) or   # Jump to offset if overflow did not occur
                (self.log and self.stora) or
                (self.log and self.storb) or
                (self.log and self.swp) or
                (self.jmp and self.shl) or
                (self.jmp and self.shr) or
                (self.jmp and self.swp) or 
                (self.jmp and self.decb))

    def Push(self, initTime):
        print("push")


    def Update(self):
        global buff
        global acc
        # always @ posedge clk
        if (not self.prevclk[0]) and (self.clk[0]):
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
                    self.t = 1
                    self.eip[0] = True
                    self.ladd[0] = True
                    #print("****EIP load****")
                elif self.t == 1:
                    self.t = 2
                    self.eip[0] = False
                    self.ladd[0] = False
                    self.ce[0] = True
                    self.linst = True
                elif self.t == 2:
                    self.ce[0] = False
                    self.linst = False
                    self.count[0] = True
                    if self.ZeroOperandOpcode():
                        # Opcode with no operand, continue to execute
                        self.t = 3
                        self.tf = True
                        #print("zero op")
                        #print("Zero operand opcode")
                    else:
                        # Fetch first operand for opcodes with 1 or more operands
                        self.t = 0
                        self.ff = True

            # First Operand Fetch
            elif self.ff:
                #print ("ff fetch")
                if self.t == 0:
                    self.ResetOutputs()
                    self.t = 1
                    self.eip[0] = True
                    self.ladd[0] = True
                elif self.t == 1:
                    self.t = 2
                    self.eip[0] = False
                    self.ladd[0] = False
                    self.ce[0] = True
                    self.lt1[0] = True
                elif self.t == 2:
                    self.count[0] = True
                    self.tf = True
                    self.ce[0] = False
                    self.lt1[0] = False
                    self.ff = False
                    if self.OneOperandOpcode():
                        # Opcode with one operand, continue to execute
                        self.t = 3
                        #print("one op")
                    else:
                        #Fetch third operand
                        self.t = 0

            # Second Operand Fetch
            elif self.tf:
                #print ("tf fetch")
                #print("t: " + str(self.t))
                if self.t == 0:
                    self.ResetOutputs()
                    self.t = 1
                    self.eip[0] = True
                    self.ladd[0] = True
                elif self.t == 1:
                    self.t = 2
                    self.eip[0] = False
                    self.ladd[0] = False
                    self.ce[0] = True
                    self.lt2[0] = True
                elif self.t == 2:
                    self.t = 3
                    self.ce[0] = False
                    self.lt2[0] = False
                    self.count[0] = True
                elif self.t >= 3:
                    if self.t == 3:
                        self.count[0] = False
                        #print("Reset count")

                    # Execute
                    if self.mov and self.immeda:
                        # MOV into A Immediate operation
                        #print ("mov")
                        if self.t == 3:
                            self.et[0] = True
                            self.lacc[0] = True
                            self.t = 4
                        elif self.t == 4:
                            self.et[0] = False
                            self.lacc[0] = False
                            self.treset = True
                    elif self.mov and self.immedb:
                        # MOV into B Immediate operation
                        if self.t == 3:
                            self.et[0] = True
                            self.lbuff[0] = True
                            self.t = 4
                        elif self.t == 4:
                            self.et[0] = False
                            self.lbuff[0] = False
                            self.treset = True
                    elif self.mov and self.stora:
                        # MOV A into MEM
                        if self.t == 3:
                            self.t = 4
                            self.et[0] = True
                            self.ladd[0] = True
                            #print("here")
                        elif self.t == 4:
                            self.t = 5
                            self.et[0] = False
                            self.ladd[0] = False
                            self.eacc[0] = True
                            self.we[0] = True
                        elif self.t == 5:
                            self.treset = True
                            self.eacc[0] = False
                            self.we[0] = False
                    elif self.mov and self.storb:
                        # MOV B into MEM
                        if self.t == 3:
                            self.t = 4
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            self.t = 5
                            self.et[0] = False
                            self.ladd[0] = False
                            self.ebuff[0] = True
                            #print("Enable B")
                            #print("Count: " + str(self.count[0]))
                            self.we[0] = True
                        elif self.t == 5:
                            self.treset = True
                            self.ebuff[0] = False
                            #print("Disable B")
                            self.we[0] = False
                    elif self.mov and self.mema:
                        # MOV MEM into A
                        if self.t == 3:
                            self.t = 4
                            #print("Set LADD")
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            self.t = 5
                            self.et[0] = False
                            self.ladd[0] = False
                            #print("Clear LADD")
                            self.ce[0] = True
                            self.lacc[0] = True
                        elif self.t == 5:
                            self.treset = True
                            self.lacc[0] = False
                            self.ce[0] = False
                            #global totalCycles
                            #print("Finish MOV MEM into A")
                    elif self.mov and self.memb:
                        # MOV MEM into B
                        if self.t == 3:
                            self.t = 4
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            self.t = 5
                            self.et[0] = False
                            self.ladd[0] = False
                            self.ce[0] = True
                            self.lbuff[0] = True
                        elif self.t == 5:
                            self.treset = True
                            self.lbuff[0] = False
                            self.ce[0] = False

                    elif self.add and self.immeda:
                        # ADD Immediate
                        if self.t == 3:
                            self.et[0] = True
                            self.lbuff[0] = True
                            self.t = 4
                        elif self.t == 4:
                            self.et[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 0
                            self.t = 5
                        elif self.t == 5:
                            self.ealu[0] = False
                            self.lacc[0] = False
                            self.treset = True
                            #print("Finish ADD Immediate")
                    elif self.add and self.mema:
                        # ADD MEM
                        if self.t == 3:
                            self.t = 4
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            self.t = 5
                            self.et[0] = False
                            self.ladd[0] = False
                            self.ce[0] = True
                            self.lbuff[0] = True
                        elif self.t == 5:
                            self.treset = True
                            self.ce[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 0
                    elif self.add and self.immedb:
                        # ADD B to A
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 0
                            #print(self.data_bus)
                        elif self.t == 4:
                            self.ealu[0] = False
                            self.lacc[0] = False
                            self.treset = True

                    elif self.sub and self.immeda:
                        # SUB Immediate
                        if self.t == 3:
                            self.et[0] = True
                            self.lbuff[0] = True
                            self.t = 4
                        elif self.t == 4:
                            self.et[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 1
                            self.t = 5
                        elif self.t == 5:
                            self.ealu[0] = False
                            self.lacc[0] = False
                            self.treset = True
                            #print("Finish SUB immediate")
                    elif self.sub and self.mema:
                        # SUB MEM
                        #print("sub mem")
                        if self.t == 3:
                            self.t = 4
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 4:
                            self.t = 5
                            self.et[0] = False
                            self.ladd[0] = False
                            self.ce[0] = True
                            self.lbuff[0] = True
                        elif self.t == 5:
                            self.treset = True
                            self.ce[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 1
                    elif self.sub and self.immedb:
                        # SUB B from A
                        #print("Sub A-B")
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 1
                        elif self.t == 4:
                            self.ealu[0] = False
                            self.lacc[0] = False
                            self.treset = True

                    elif self.swp and self.mov:
                        # Swap A and B
                        if self.t == 3:
                            #print("Start SWP")
                            self.t = 4
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 4:
                            self.t = 5
                            self.eacc[0] = False
                            self.lt1[0] = False
                            self.ebuff[0] = True
                            self.lacc[0] = True
                        elif self.t == 5:
                            self.t = 6
                            self.ebuff[0] = False
                            self.lacc[0] = False
                            self.lbuff[0] = True
                            self.et[0] = True
                        elif self.t == 6:
                            self.treset = True
                            self.lbuff[0] = False
                            self.et[0] = False
                            #print("Finish swap")

                    elif self.jmp and self.mema:
                        # JMP (Jump unconditional)
                        if self.t == 3:
                            self.t = 4
                            self.et[0] = True
                            self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
                            self.et[0] = False
                            self.lip[0] = False
                    elif self.jz and self.mema:
                        # JZ (Jump if zero)
                        if self.t == 3:
                            self.t = 4
                            if self.zf[0]:
                                self.et[0] = True
                                self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
                            self.et[0] = False
                            self.lip[0] = False
                    elif self.jnz and self.mema:
                        # JNZ (Jump if not zero)
                        if self.t == 3:
                            self.t = 4
                            if not self.zf[0]:
                                self.et[0] = True
                                self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
                            self.et[0] = False
                            self.lip[0] = False
                            #print("Finish JNZ")
                    elif self.jm and self.mema:
                        # JM (Jump if minus)
                        if self.t == 3:
                            self.t = 4
                            if self.sf[0]:
                                self.et[0] = True
                                self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
                            self.et[0] = False
                            self.lip[0] = False
                    elif self.jp and self.mema:
                        # JP (Jump if positive)
                        if self.t == 3:
                            self.t = 4
                            if not self.sf[0]:
                                self.et[0] = True
                                self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
                            self.et[0] = False
                            self.lip[0] = False
                    elif self.jc and self.mema:
                        # JC (Jump if carry)
                        if self.t == 3:
                            self.t = 4
                            if self.cf[0]:
                                self.et[0] = True
                                self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
                            self.et[0] = False
                            self.lip[0] = False
                    elif self.jnc and self.mema:
                        # JNC (Jump if not carry)
                        if self.t == 3:
                            self.t = 4
                            if not self.cf[0]:
                                self.et[0] = True
                                self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
                            self.et[0] = False
                            self.lip[0] = False
                    elif self.jc and self.memb:
                        # JOF (Jump if overflow)
                        if self.t == 3:
                            self.t = 4
                            if self.of[0]:
                                self.et[0] = True
                                self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
                            self.et[0] = False
                            self.lip[0] = False
                    elif self.jnc and self.memb:
                        # JNOF (Jump if not overflow)
                        if self.t == 3:
                            self.t = 4
                            if not self.of[0]:
                                self.et[0] = True
                                self.lip[0] = True
                        elif self.t == 4:
                            self.treset = True
                            self.et[0] = False
                            self.lip[0] = False

                    elif self.log and self.shl:
                        # SHL (Left shift)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 2
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                    elif self.log and self.shr:
                        # SHR (Right shift)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 3
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                    elif self.log and self.inca:
                        # INC A (Increment A)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 4
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                    elif self.log and self.deca:
                        # DEC A (Decrement A)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 5
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                    elif self.log and self.incb:
                        # INC B (Increment B)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lbuff[0] = True
                            self.sel[0] = 6
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lbuff[0] = False
                    elif self.log and self.decb:
                        # DEC B (Decrement B)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lbuff[0] = True
                            self.sel[0] = 7
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lbuff[0] = False
                            #print("FINISH DEC B")
                    elif self.log and self.mema:
                        # AND B (AND A and B)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 8
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                    elif self.log and self.stora:
                        # AND IMMED (AND A and immediate value)
                        if self.t == 3:
                            self.t = 4
                            self.et[0] = True
                            self.lbuff[0] = True
                        elif self.t == 4:
                            self.t = 5
                            self.et[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 8
                        elif self.t == 5:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                    elif self.log and self.memb:
                        # OR B (OR A and B)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 9
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                    elif self.log and self.storb:
                        # OR IMMED (OR A and immediate value)
                        if self.t == 3:
                            self.t = 4
                            self.et[0] = True
                            self.lbuff[0] = True
                        elif self.t == 4:
                            self.t = 5
                            self.et[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 9
                        elif self.t == 5:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                    elif self.log and self.immeda:
                        # XOR B (XOR A and B)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 0xA
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                    elif self.log and self.swp:
                        # XOR IMMED (XOR A and immediate value)
                        if self.t == 3:
                            self.t = 4
                            self.et[0] = True
                            self.lbuff[0] = True
                            #print("XOR enable lbuff")
                        elif self.t == 4:
                            self.t = 5
                            self.et[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 0xA
                        elif self.t == 5:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False
                            #print("Finish XOR immed")
                    elif self.log and self.immedb:
                        # NOT (NOT A)
                        if self.t == 3:
                            self.t = 4
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.sel[0] = 0xB
                        elif self.t == 4:
                            self.treset = True
                            self.ealu[0] = False
                            self.lacc[0] = False

                    elif self.io and self.mema:
                        # IO A
                        if self.t == 3:
                            self.treset = True
                            print("Clock cycles: " + str(totalCycles))
                            print("A REG: " + str(format(acc.data[0], '#x')))
                    elif self.io and self.memb:
                        # IO B
                        if self.t == 3:
                            self.treset = True
                            print("Clock cycles: " + str(totalCycles))
                            print("B REG: " + str(format(buff.data[0], '#x')))

                    # CALL Function
                    elif self.jmp and self.stora:
                        if self.t == 3:
                            # Save A
                            self.t = 4
                            self.lrr1[0] = True
                            self.eacc[0] = True
                        elif self.t == 4:
                            # Save B
                            self.t = 5
                            self.lrr1[0] = False
                            self.eacc[0] = False
                            self.lrr2[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            ## Load low byte of stack pointer into A
                            self.t = 6
                            self.lrr2[0] = False
                            self.ebuff[0] = False
                            self.lacc[0] = True
                            self.esp[0] = True
                        elif self.t == 6:
                            # Load high byte of stack pointer into B
                            self.t = 7
                            self.lacc[0] = False
                            self.esp[0] = False
                            self.esp_b[0] = True
                            self.lbuff[0] = True

                        elif self.t == 7:
                            # Increment lower byte of stack pointer in A
                            self.t = 8
                            self.esp_b[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 8:
                            # Increment upper byte of stack pointer in B if carry
                            self.t = 9
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 9:
                            # Load new SP into address register
                            self.t = 10
                            self.lbuff[0] = False
                            self.ealu[0] = False
                            self.lsp2[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True

                        elif self.t == 10:
                            # Write lower byte of IP to stack
                            self.t = 11
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.we[0] = True
                            self.eip[0] = True

                        elif self.t == 11:
                            # Increment lower byte of stack pointer in A
                            self.t = 12
                            self.we[0] = False
                            self.eip[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 12:
                            # Increment upper byte of stack pointer in B if carry
                            self.t = 13
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 13:
                            # Load new SP into address register
                            self.t = 14
                            self.lbuff[0] = False
                            self.ealu[0] = False
                            self.lsp2[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True
                        elif self.t == 14:
                            # Write upper byte of IP to stack
                            self.t = 15
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.we[0] = True
                            self.eip_b[0] = True

                        elif self.t == 15:
                            # Increment lower byte of stack pointer in A
                            self.t = 16
                            self.we[0] = False
                            self.eip_b[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 16:
                            # Increment upper byte of stack pointer in B if carry
                            self.t = 17
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 17:
                            # Load new SP into address register
                            self.t = 18
                            self.lbuff[0] = False
                            self.ealu[0] = False
                            self.lsp2[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True

                        elif self.t == 18:
                            # Set BP to SP
                            self.t = 19
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.lbpa[0] = True
                            self.esp[0] = True

                        elif self.t == 19:
                            # Save lower byte of BP to stack
                            self.t = 20
                            self.lbpa[0] = False
                            self.esp[0] = False
                            self.we[0] = True
                            self.ebp[0] = True

                        elif self.t == 20:
                            # Increment lower byte of stack pointer in A
                            self.t = 21
                            self.we[0] = False
                            self.ebp[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 21:
                            # Increment upper byte of stack pointer in B if carry
                            self.t = 22
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6
                        elif self.t == 22:
                            # Load new SP into address register
                            self.t = 23
                            self.lbuff[0] = False
                            self.ealu[0] = False
                            self.lsp2[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True
                        elif self.t == 23:
                            # Save upper byte of BP to stack
                            self.t = 24
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.we[0] = True
                            self.ebp_b[0] = True

                        elif self.t == 24:
                            # Set IP to be call address
                            self.t = 25
                            self.we[0] = False
                            self.ebp_b[0] = False
                            self.lip[0] = True
                            self.et[0] = True

                        elif self.t == 25:
                            # Restore A
                            self.t = 26
                            self.lip[0] = False
                            self.et[0] = False
                            self.err[0] = True
                            self.lacc[0] = True

                        elif self.t == 26:
                            # Restore B
                            self.t = 27
                            self.err[0] = False
                            self.lacc[0] = False
                            self.err_b[0] = True
                            self.lbuff[0] = True

                        elif self.t == 27:
                            # Call finished
                            self.err_b[0] = False
                            self.lbuff[0] = False
                            self.treset = True


                    # Return from Function
                    elif self.jmp and self.storb:
                        if self.t == 3:
                            # Save A
                            self.t = 4
                            self.lrr1[0] = True
                            self.eacc[0] = True
                        elif self.t == 4:
                            # Save B
                            self.t = 5
                            #print ("Saved A: " + hex(self.data_bus[0]))
                            self.lrr1[0] = False
                            self.eacc[0] = False
                            self.lrr2[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            ## Load low byte of stack pointer into A
                            self.t = 6
                            #print ("Saved B: " + hex(self.data_bus[0]))
                            self.lrr2[0] = False
                            self.ebuff[0] = False
                            self.lacc[0] = True
                            self.esp[0] = True
                        elif self.t == 6:
                            # Load high byte of stack pointer into B
                            self.t = 7
                            self.lacc[0] = False
                            self.esp[0] = False
                            self.esp_b[0] = True
                            self.lbuff[0] = True

                        elif self.t == 7:
                            # Load SP into address register
                            self.t = 8
                            self.esp_b[0] = False
                            self.lbuff[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True

                        elif self.t == 8:
                            # Load upper byte of BP from stack
                            self.t = 9
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.ce[0] = True
                            self.lbp2[0] = True
                            #print ("SP into ADR: " + hex(self.adr_bus[0]))

                        elif self.t == 9:
                            # Decrement lower byte of stack pointer in A
                            self.t = 10
                            self.ce[0] = False
                            self.lbp2[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 10:
                            # Decrement upper byte of stack pointer in B if carry
                            self.t = 11
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 7

                        elif self.t == 11:
                            # Load SP into address register
                            self.t = 12
                            self.esp_b[0] = False
                            self.lbuff[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True
                        elif self.t == 12:
                            # Load lower byte of BP from stack
                            self.t = 13
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.ce[0] = True
                            self.lbp1[0] = True

                        elif self.t == 13:
                            # Decrement lower byte of stack pointer in A
                            self.t = 14
                            self.ce[0] = False
                            self.lbp1[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 14:
                            # Decrement upper byte of stack pointer in B if carry
                            self.t = 15
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 7

                        elif self.t == 15:
                            # Load SP into address register
                            self.t = 16
                            self.esp_b[0] = False
                            self.lbuff[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True
                        elif self.t == 16:
                            # Load upper byte of IP from stack
                            self.t = 17
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.ce[0] = True
                            self.lip2[0] = True

                        elif self.t == 17:
                            # Decrement lower byte of stack pointer in A
                            self.t = 18
                            self.ce[0] = False
                            self.lip2[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 18:
                            # Decrement upper byte of stack pointer in B if carry
                            self.t = 19
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 7

                        elif self.t == 19:
                            # Load SP into address register
                            self.t = 20
                            self.esp_b[0] = False
                            self.lbuff[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True
                        elif self.t == 20:
                            # Load lower byte of IP from stack
                            self.t = 21
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.ce[0] = True
                            self.lip1[0] = True

                        elif self.t == 21:
                            # Decrement lower byte of stack pointer in A
                            self.t = 22
                            self.ce[0] = False
                            self.lip1[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 22:
                            # Decrement upper byte of stack pointer in B if carry
                            self.t = 23
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 7

                        elif self.t == 23:
                            # Restore A
                            self.t = 24
                            self.lbuff[0] = False
                            self.ealu[0] = False
                            self.lsp2[0] = False
                            self.err[0] = True
                            self.lacc[0] = True

                        elif self.t == 24:
                            # Restore B
                            self.t = 25
                            #print ("Restored A: " + hex(self.data_bus[0]))
                            self.err[0] = False
                            self.lacc[0] = False
                            self.err_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 25:
                            # Call finished
                            #print ("Restored B: " + hex(self.data_bus[0]))
                            self.lbuff[0] = False
                            self.err_b[0] = False
                            self.treset = True

                    # Peek at <immed> BP offset
                    elif self.jmp and self.shl:
                        if self.t == 3:
                         # Save B
                            self.t = 4
                            self.lrr1[0] = True
                            self.ebuff[0] = True
                        elif self.t == 4:
                            # Load low byte of base pointer into A
                            self.t = 5
                            self.lrr1[0] = False
                            self.ebuff[0] = False
                            self.lacc[0] = True
                            self.ebp[0] = True
                        elif self.t == 5:
                            # Load offset into B
                            self.t = 6
                            self.lacc[0] = False
                            self.ebp[0] = False
                            self.lbuff[0] = True
                            self.et[0] = True
                        elif self.t == 6:
                            # Add A and B
                            self.t = 7
                            self.lbuff[0] = False
                            self.et[0] = False
                            self.lacc[0] = True
                            self.ealu[0] = True
                            self.sel[0] = 0
                        elif self.t == 7:
                            # Move result to temp1
                            self.t = 8
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 8:
                            # Load BP2 into A
                            self.t = 9
                            self.eacc[0] = False
                            self.lt1[0] = False
                            self.ebp_b[0] = True
                            self.lacc[0] = True
                        elif self.t == 9:
                            # Decide if upper byte of BP needs to be incremented
                            self.t = 10
                            self.ebp_b[0] = False
                            self.lacc[0] = False
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
                            self.t = 11
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.eacc[0] = True
                            self.lt2[0] = True
                        elif self.t == 11:
                            # Move temp into address reg
                            self.t = 12
                            #print("ACC: " + hex(self.data_bus[0]))
                            self.eacc[0] = False
                            self.lt2[0] = False
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 12:
                            # Move output into A
                            self.t = 13
                            self.et[0] = False
                            self.ladd[0] = False
                            self.lacc[0] = True
                            self.ce[0] = True

                        elif self.t == 13:
                            # Restore B
                            self.t = 14
                            self.ce[0] = False
                            self.lacc[0] = False
                            self.err[0] = True
                            self.lbuff[0] = True
                        elif self.t == 14:
                            # Call finished
                            self.lbuff[0] = False
                            self.err[0] = False
                            self.treset = True

                    # Peek at A reg BP offset
                    elif self.jmp and self.aux:
                        #print("A reg peek")
                        if self.t == 3:
                            # Save A
                            self.t = 4
                            self.lrr2[0] = True
                            self.eacc[0] = True
                        elif self.t == 4:
                         # Save B
                            self.t = 5
                            print("Saved A: " + hex(self.data_bus[0]))
                            self.lrr2[0] = False
                            self.eacc[0] = False
                            self.lrr1[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            # Load low byte of base pointer into A
                            self.t = 6
                            self.lrr1[0] = False
                            self.ebuff[0] = False
                            self.lacc[0] = True
                            self.ebp[0] = True
                        elif self.t == 6:
                            # Load offset into B
                            self.t = 7
                            self.lacc[0] = False
                            self.ebp[0] = False
                            self.lbuff[0] = True
                            self.err_b[0] = True
                        elif self.t == 7:
                            # Add A and B
                            self.t = 8
                            print("Offset: " + hex(self.data_bus[0]))
                            self.lbuff[0] = False
                            self.err_b[0] = False
                            self.lacc[0] = True
                            self.ealu[0] = True
                            self.sel[0] = 0
                        elif self.t == 8:
                            # Move result to temp1
                            self.t = 9
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 9:
                            # Load BP2 into A
                            self.t = 10
                            self.eacc[0] = False
                            self.lt1[0] = False
                            self.ebp_b[0] = True
                            self.lacc[0] = True
                        elif self.t == 10:
                            # Decide if upper byte of BP needs to be incremented
                            self.t = 11
                            self.ebp_b[0] = False
                            self.lacc[0] = False
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
                            self.t = 12
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.eacc[0] = True
                            self.lt2[0] = True
                        elif self.t == 12:
                            # Move temp into address reg
                            self.t = 13
                            #print("ACC: " + hex(self.data_bus[0]))
                            self.eacc[0] = False
                            self.lt2[0] = False
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 13:
                            # Move output into A
                            self.t = 14
                            self.et[0] = False
                            self.ladd[0] = False
                            self.lacc[0] = True
                            self.ce[0] = True

                        elif self.t == 14:
                            # Restore B
                            self.t = 15
                            self.ce[0] = False
                            self.lacc[0] = False
                            self.err[0] = True
                            self.lbuff[0] = True
                        elif self.t == 15:
                            # Call finished
                            self.lbuff[0] = False
                            self.err[0] = False
                            self.treset = True
                            

                    # Poke A to BP offset
                    elif self.jmp and self.shr:
                        if self.t == 3:
                         # Save A to RR2
                            self.t = 4
                            self.eacc[0] = True
                            self.lrr2[0] = True
                        elif self.t == 4:
                         # Save B to RR1
                            #print("Saved A: " + hex(self.data_bus[0]))
                            self.t = 5
                            self.eacc[0] = False
                            self.lrr2[0] = False
                            self.lrr1[0] = True
                            self.ebuff[0] = True
                        elif self.t == 5:
                            # Load low byte of base pointer into A
                            self.t = 6
                            self.lrr1[0] = False
                            self.ebuff[0] = False
                            self.lacc[0] = True
                            self.ebp[0] = True
                        elif self.t == 6:
                            # Load offset into B
                            self.t = 7
                            self.lacc[0] = False
                            self.ebp[0] = False
                            self.lbuff[0] = True
                            self.et[0] = True
                        elif self.t == 7:
                            # Add A and B
                            self.t = 8
                            self.lbuff[0] = False
                            self.et[0] = False
                            self.lacc[0] = True
                            self.ealu[0] = True
                            self.sel[0] = 0
                        elif self.t == 8:
                            # Move result to temp1
                            self.t = 9
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.eacc[0] = True
                            self.lt1[0] = True
                        elif self.t == 9:
                            # Load BP2 into A
                            self.t = 10
                            self.eacc[0] = False
                            self.lt1[0] = False
                            self.ebp_b[0] = True
                            self.lacc[0] = True
                        elif self.t == 10:
                            # Decide if upper byte of BP needs to be incremented
                            self.t = 11
                            self.ebp_b[0] = False
                            self.lacc[0] = False
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
                            self.t = 12
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.eacc[0] = True
                            self.lt2[0] = True
                        elif self.t == 12:
                            # Move temp into address reg
                            self.t = 13
                            #print("ACC: " + hex(self.data_bus[0]))
                            self.eacc[0] = False
                            self.lt2[0] = False
                            self.et[0] = True
                            self.ladd[0] = True
                        elif self.t == 13:
                            # Write saved value of A and restore A
                            self.t = 14
                            self.et[0] = False
                            self.ladd[0] = False
                            self.err_b[0] = True
                            self.we[0] = True
                            self.lacc[0] = True

                        elif self.t == 14:
                            # Restore B
                            self.t = 15
                            #print("Saved A: " + hex(self.data_bus[0]))
                            self.err_b[0] = False
                            self.we[0] = False
                            self.lacc[0] = False
                            self.err[0] = True
                            self.lbuff[0] = True
                        elif self.t == 15:
                            # Call finished
                            self.lbuff[0] = False
                            self.err[0] = False
                            self.treset = True
                            #print("finish poke")

                    # Pop from SP
                    elif self.jmp and self.deca:
                        if self.t == 3:
                         # Save B
                            self.t = 4
                            self.lrr1[0] = True
                            self.ebuff[0] = True
                        elif self.t == 4:
                            # Load stack pointer into address reg and A
                            self.t = 5
                            self.lrr1[0] = False
                            self.ebuff[0] = False
                            self.lacc[0] = True
                            self.esp[0] = True
                            self.ladd[0] = True
                        elif self.t == 5:
                            # Move output into RR2
                            self.t = 6
                            self.lacc[0] = False
                            self.esp[0] = False
                            self.ladd[0] = False
                            self.lrr2[0] = True
                            self.ce[0] = True
                        elif self.t == 6:
                            # Load high byte of stack pointer into B
                            self.t = 7
                            self.lrr2[0] = False
                            self.ce[0] = False
                            self.esp_b[0] = True
                            self.lbuff[0] = True

                        elif self.t == 7:
                            # Decrement lower byte of stack pointer in A
                            self.t = 8
                            self.esp_b[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 5
                        elif self.t == 8:
                            # Decrement upper byte of stack pointer in B if carry
                            self.t = 9
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 7

                        elif self.t == 9:
                            # Move saved value from RR2 to A
                            self.t = 10
                            self.lbuff[0] = False
                            self.ealu[0] = False
                            self.lsp2[0] = False
                            self.err_b[0] = True
                            self.lacc[0] = True
                        elif self.t == 10:
                            # Restore B
                            self.t = 11
                            self.err_b[0] = False
                            self.lacc[0] = False
                            self.err[0] = True
                            self.lbuff[0] = True
                        elif self.t == 11:
                            # Pop finished
                            self.lbuff[0] = False
                            self.err[0] = False
                            self.treset = True

                    # Push A reg to SP
                    elif self.jmp and self.decb:
                        if self.t == 3:
                         # Save A
                            self.t = 4
                            self.lrr1[0] = True
                            self.eacc[0] = True
                        elif self.t == 4:
                         # Save B
                            self.t = 5
                            self.lrr1[0] = False
                            self.eacc[0] = False
                            self.lrr2[0] = True
                            self.ebuff[0] = True

                        elif self.t == 5:
                            # Load stack pointer lower byte into A
                            self.t = 6
                            self.lrr2[0] = False
                            self.ebuff[0] = False
                            self.lacc[0] = True
                            self.esp[0] = True

                        elif self.t == 6:
                            # Load high byte of stack pointer into B
                            self.t = 7
                            self.lacc[0] = False
                            self.esp[0] = False
                            self.esp_b[0] = True
                            self.lbuff[0] = True

                        elif self.t == 7:
                            # Increment lower byte of stack pointer in A
                            self.t = 8
                            self.esp_b[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 8:
                            # Increment upper byte of stack pointer in B if carry
                            self.t = 9
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6

                        elif self.t == 9:
                            # Load stack pointer into address register
                            self.t = 10
                            self.lbuff[0] = False
                            self.ealu[0] = False
                            self.lsp2[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True
                        
                        elif self.t == 10:
                            # Write saved A in RR1 to SP
                            self.t = 11
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.err[0] = True
                            self.we[0] = True
                        
                        elif self.t == 11:
                            # Restore B
                            self.t = 12
                            self.err[0] = False
                            self.we[0] = False
                            self.err_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 12:
                            # Push finished
                            self.err_b[0] = False
                            self.lbuff[0] = False
                            self.treset = True

                    # Push <immed> to SP
                    elif self.jmp and self.swp:
                        if self.t == 3:
                         # Save A
                            self.t = 4
                            self.lrr1[0] = True
                            self.eacc[0] = True
                        elif self.t == 4:
                         # Save B
                            self.t = 5
                            self.lrr1[0] = False
                            self.eacc[0] = False
                            self.lrr2[0] = True
                            self.ebuff[0] = True

                        elif self.t == 5:
                            # Load stack pointer lower byte into A
                            self.t = 6
                            self.lrr2[0] = False
                            self.ebuff[0] = False
                            self.lacc[0] = True
                            self.esp[0] = True

                        elif self.t == 6:
                            # Load high byte of stack pointer into B
                            self.t = 7
                            self.lacc[0] = False
                            self.esp[0] = False
                            self.esp_b[0] = True
                            self.lbuff[0] = True

                        elif self.t == 7:
                            # Increment lower byte of stack pointer in A
                            self.t = 8
                            self.esp_b[0] = False
                            self.lbuff[0] = False
                            self.ealu[0] = True
                            self.lacc[0] = True
                            self.lsp1[0] = True
                            self.sel[0] = 4
                        elif self.t == 8:
                            # Increment upper byte of stack pointer in B if carry
                            self.t = 9
                            self.lacc[0] = False
                            self.ealu[0] = False
                            self.lsp1[0] = False
                            if self.cf[0]:
                                self.lbuff[0] = True
                                self.ealu[0] = True
                                self.lsp2[0] = True
                                self.sel[0] = 6

                        elif self.t == 9:
                            # Load stack pointer into address register
                            self.t = 10
                            self.lbuff[0] = False
                            self.ealu[0] = False
                            self.lsp2[0] = False
                            self.ladd[0] = True
                            self.esp[0] = True
                        
                        elif self.t == 10:
                            # Write <immed> to SP
                            self.t = 11
                            self.ladd[0] = False
                            self.esp[0] = False
                            self.et[0] = True
                            self.we[0] = True
                        
                        elif self.t == 11:
                            # Restore B
                            self.t = 12
                            self.et[0] = False
                            self.we[0] = False
                            self.err_b[0] = True
                            self.lbuff[0] = True
                        elif self.t == 12:
                            # Push finished
                            self.err_b[0] = False
                            self.lbuff[0] = False
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
alu = arithmetic_logic_unit(clk, data_bus, acc_alu_out, buff_alu_out, sel, ealu, cf, zf, sf, of, xf)
acc = ab_register(lacc, eacc, clk, data_bus, acc_alu_out)
buff = ab_register(lbuff, ebuff, clk, data_bus, buff_alu_out)
irc = instruction_register_control(clk, data_bus, adr_bus, reset, go, eip, eip_b, ladd, ce, count, lt1, lt2, lta, we, lip, lip1, lip2, et, et_b, lsp1, lsp2, lspa, esp, esp_b, lbp1, lbp2, lbpa, ebp, ebp_b, lrr1, lrr2, lrra, err, err_b, lacc, eacc, lbuff, ebuff, sel, ealu, cf, zf, sf, of, xf)

display = Graphics_Display(charMem, screenMem, 0, canvas, SCREEN_WIDTH, SCREEN_HEIGHT, PIXEL_SCALE)

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
        file.write("      0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\n")
        while i < RAM_SIZE_BYTES:
            file.write(f"{i:#0{numZeros}x}" + ": ")
            for j in range(16):
                file.write(f"{ab.memory[i+j]:02x}" + " ")

            file.write("\n")
            i += 16



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
    while (totalCycles < 100000) and not systemHalt:
        totalCycles += 1
        Toggle_Clk()
        if (totalCycles % 5000 == 0):
            display.update()
            ws.update()

    endTime = time.time_ns()
    #print("End time: " + str(endTime))
    deltaTime = endTime - startTime
    #print("ns taken: " + str(deltaTime))
    #print("Real clock rate: " + str(1000000000*totalCycles/deltaTime))

    display.update()
    Print_Final_Dump()
    Dump_Memory()
    ws.mainloop()

TestBench2()
