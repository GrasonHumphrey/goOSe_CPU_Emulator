from array import array
from tkinter import *

class Graphics_Display:
    def __init__(self, charMem, screenMem, mode, canvas: Canvas, width, height, pixelScale):
        self.charMem = charMem
        self.screenMem = screenMem
        self.mode = mode
        self.canvas = canvas
        self.width = width
        self.height = height
        self.pixelScale = pixelScale
        self.pixels = []
        self.oldCharMem = []
        self.oldScreenMem = []
        
        # Copy data from char ROM into charMem RAM
        data = array('B')
        with open('char_rom.bin', 'rb') as f:
            data.fromfile(f, 0x1000)
        for i in range(0x1000):
            self.charMem[i] = data[i]
            self.oldCharMem.append(data[i])

        if (self.mode == 0):
            # Set screen mem to all char blanks
            for i in range(0x400):
                self.screenMem[i] = 0x60
                self.oldScreenMem.append(0x60)

        # Create all pixels
        for i in range(0x400):
            charLine = 0
            while (charLine < 8):
                for pixel in range(8):
                    rect = self.canvas.create_rectangle(
                        (i*8*self.pixelScale) % self.width + pixel*self.pixelScale + 1, 
                        int(i*8*self.pixelScale/self.height)*8*self.pixelScale + charLine*self.pixelScale + 2, 
                        (i*8*self.pixelScale) % self.width + pixel*self.pixelScale + self.pixelScale + 1, 
                        int(i*8*self.pixelScale/self.height)*8*self.pixelScale + charLine*self.pixelScale + self.pixelScale + 2,
                        outline="#000",
                        fill="#000",
                        width=0)
                    self.pixels.append(rect)
                charLine += 1
                
    def is_bit_set(self, x, n):
        #print(str(x & 1 << n != 0))
        return x & 1 << n != 0

    def update(self):
        #self.mode = mode
        if (self.mode == 0):
            # Character graphics mode
            for i in range(0x400):
                charCode = self.screenMem[i] 
                charLine = 0
                while (charLine < 8):
                    if (charCode != self.oldScreenMem[i] or self.charMem[8 * charCode + charLine] != self.oldCharMem[8 * charCode + charLine]):
                        # Only update pixel if either screen or character memory has been updated
                        self.oldCharMem[8 * charCode + charLine] = self.charMem[8 * charCode + charLine]
                        #print(hex(charCode))
                        for pixel in range(8):
                            if (self.is_bit_set(self.charMem[8 * charCode + charLine], 7-pixel)):
                                self.canvas.itemconfig(self.pixels[i*64+charLine*8+pixel], fill="#0ff")
                            else:
                                self.canvas.itemconfig(self.pixels[i*64+charLine*8+pixel], fill="#000")
                    charLine += 1
                self.oldScreenMem[i] = charCode