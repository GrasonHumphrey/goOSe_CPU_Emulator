from array import array
from tkinter import *

screenModeLoc = 0x400
colorLoc0 = 0x401
colorLoc1 = 0x402
colorLoc2 = 0x403
colorLoc3 = 0x404

class Graphics_Display:

    def GetColor(self, code):
        if (code == 0x00):
            # Black
            return '#000000'
        elif (code == 0x1):
            # White
            return '#FFFFFF'
        elif (code == 0x2):
            # Red
            return '#880000' 
        elif (code == 0x3):
            # Cyan
            return '#00FFFF' 
        elif (code == 0x4):
            # Purple
            return '#CC44CC' 
        elif (code == 0x5):
            # Green
            return '#00CC55' 
        elif (code == 0x6):
            # Blue
            return '#0000AA' 
        elif (code == 0x7):
            # Yellow
            return '#EEEE77' 
        elif (code == 0x8):
            # Orange
            return '#DD8855' 
        elif (code == 0x9):
            # Brown
            return '#664400' 
        elif (code == 0xA):
            # Light red
            return '#FF7777' 
        elif (code == 0xB):
            # Dark Grey
            return '#333333' 
        elif (code == 0xC):
            # Med Grey
            return '#777777' 
        elif (code == 0xD):
            # Light Green
            return '#AAFF66' 
        elif (code == 0xE):
            # Light Blue
            return '#0088FF' 
        elif (code == 0xF):
            # Light Grey
            return '#BBBBBB' 
        
    def __init__(self, charMem, screenMem, colorMem, mode, canvas: Canvas, width, height, pixelScale):
        self.charMem = charMem
        self.screenMem = screenMem
        self.colorMem = colorMem
        #self.mode = mode
        self.canvas = canvas
        self.width = width
        self.height = height
        self.pixelScale = pixelScale
        self.pixels = []
        self.oldCharMem = []
        self.oldScreenMem = []
        self.oldColorMem = []
        self.oldColor = 0x04
        
        # Copy data from char ROM into charMem RAM
        data = array('B')
        with open('char_rom.bin', 'rb') as f:
            data.fromfile(f, 0x1000)
        for i in range(0x1000):
            self.charMem[i] = data[i]
            self.oldCharMem.append(data[i])

        if (mode == 0):
            # Set screen mem to all char blanks
            for i in range(0x400):
                self.screenMem[i] = 0x00
                self.oldScreenMem.append(0x00)

        # Set screen mode to character
        self.colorMem[screenModeLoc] = mode
        # Set BG color to black and text to cyan
        self.colorMem[colorLoc0] = 0x0
        self.colorMem[colorLoc1] = 0x3
        self.oldColorMem = self.colorMem.copy()

        # Create all pixels and color RAM
        for i in range(0x400):
            self.colorMem[i] = (self.colorMem[colorLoc1])
            #print(self.colorMem[i])
            charLine = 0
            while (charLine < 8):
                for pixel in range(8):
                    # Set initial BG color
                    newColor = self.GetColor(self.colorMem[colorLoc0])
                    #print(newColor)
                    rect = self.canvas.create_rectangle(
                        (i*8*self.pixelScale) % self.width + pixel*self.pixelScale + 1, 
                        int(i*8*self.pixelScale/self.height)*8*self.pixelScale + charLine*self.pixelScale + 2, 
                        (i*8*self.pixelScale) % self.width + pixel*self.pixelScale + self.pixelScale + 1, 
                        int(i*8*self.pixelScale/self.height)*8*self.pixelScale + charLine*self.pixelScale + self.pixelScale + 2,
                        outline=newColor,
                        fill=newColor,
                        width=0)
                    self.pixels.append(rect)
                charLine += 1
        
        #print(self.GetColor(self.colorMem[colorLoc1] & 0xF0 >> 4))
                
    def is_bit_set(self, x, n):
        #print(str(x & 1 << n != 0))
        return x & 1 << n != 0
    
    def get_bit_pair(self, x, pair):
        #print ((x & (3 << (pair * 2))) >> (pair * 2))
        return ((x & (3 << (pair * 2))) >> (pair * 2))

    def update(self):
        #self.mode = mode
        if (self.colorMem[screenModeLoc] == 0 or self.colorMem[screenModeLoc] == 1):

            # Character graphics mode
            for i in range(0x400):
                charCode = self.screenMem[i] 
                charLine = 0
                while (charLine < 8):
                    if (charCode != self.oldScreenMem[i] or 
                        self.charMem[8 * charCode:8 * charCode + 8] != self.oldCharMem[8 * charCode: 8 * charCode + 8] or 
                        self.colorMem[i] != self.oldColorMem[i] or 
                        self.colorMem[colorLoc0] != self.oldColorMem[colorLoc0] or
                        self.colorMem[screenModeLoc] != self.oldColorMem[screenModeLoc]):
                        # Only update pixel if either screen or character memory has been updated
                        #print(hex(charCode))
                        if self.colorMem[screenModeLoc] == 0:
                            for pixel in range(8):
                                fillColor = '#000000'
                                if (self.is_bit_set(self.charMem[8 * charCode + charLine], 7-pixel)):
                                    fillColor = self.GetColor(self.colorMem[i])
                                else:
                                    # Fill with BG color
                                    fillColor = self.GetColor(self.colorMem[colorLoc0])
                                self.canvas.itemconfig(self.pixels[i*64+charLine*8+pixel], fill=fillColor)
                        elif self.colorMem[screenModeLoc] == 1:
                            for pair in range(4):
                                pairVal = self.get_bit_pair(self.charMem[8 * charCode + charLine], 3-pair)
                                fillColor = '#000000'
                                if (pairVal == 0):
                                    # Fill with BG color
                                    fillColor = self.GetColor(self.colorMem[colorLoc0])
                                elif (pairVal == 1):
                                    # Color 2
                                    fillColor = self.GetColor(self.colorMem[colorLoc1])
                                elif (pairVal == 2):
                                    # Color 3
                                    fillColor = self.GetColor(self.colorMem[colorLoc2])
                                elif (pairVal == 3):
                                    # Color 3
                                    fillColor = self.GetColor(self.colorMem[colorLoc3])
                                self.canvas.itemconfig(self.pixels[i*64+charLine*8+pair*2], fill=fillColor)
                                self.canvas.itemconfig(self.pixels[i*64+charLine*8+pair*2+1], fill=fillColor)


                    charLine += 1
                self.oldScreenMem[i] = charCode
                #self.oldColorMem[i] = self.colorMem[i]
                
            if (self.oldCharMem != self.charMem):
                self.oldCharMem = self.charMem.copy()
                #print("char mem copy")
            if (self.colorMem != self.oldColorMem):
                self.oldColorMem = self.colorMem.copy()
                #print("color mem copy")
