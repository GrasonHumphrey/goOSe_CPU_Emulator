from array import array
class Graphics_Display:
    def __init__(self, charMem, screenMem, mode, canvas, width, height, pixelScale):
        self.charMem = charMem
        self.screenMem = screenMem
        self.mode = mode
        self.canvas = canvas
        self.width = width
        self.height = height
        self.pixelScale = pixelScale
        
        # Copy data from char ROM into charMem RAM
        data = array('B')
        with open('char_rom.bin', 'rb') as f:
            data.fromfile(f, 0x1000)
        for i in range(0x1000):
            self.charMem[i] = data[i]

        # Set screen mem to all char blanks
        for i in range(0x400):
            self.screenMem[i] = 0x60
            #self.screenMem[i] = 0x01
        
    def is_bit_set(self, x, n):
        #print(str(x & 1 << n != 0))
        return x & 1 << n != 0

    def update(self):
        #self.mode = mode
        if (self.mode == 0):
            # Character graphics mode
            for i in range(0x400):
                charCode = self.screenMem[i]
                if (charCode != 0x20 and charCode != 0x60):
                    charLine = 0
                    while (charLine < 8):
                        for pixel in range(8):
                            if (self.is_bit_set(self.charMem[8 * charCode + charLine], 7-pixel)):
                                self.canvas.create_rectangle(
                                        (i*8*self.pixelScale) % self.width + pixel*self.pixelScale + 1, 
                                        int(i*8*self.pixelScale/self.height)*8*self.pixelScale + charLine*self.pixelScale + 2, 
                                        (i*8*self.pixelScale) % self.width + pixel*self.pixelScale + self.pixelScale + 1, 
                                        int(i*8*self.pixelScale/self.height)*8*self.pixelScale + charLine*self.pixelScale + self.pixelScale + 2,
                                        outline="#0ff",
                                        fill="#0ff",
                                        width=0)
                                #print(str((i*8*self.pixelScale) % self.width + pixel))
                        charLine += 1