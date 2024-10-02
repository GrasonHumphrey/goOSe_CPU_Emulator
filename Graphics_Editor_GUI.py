# goOSe graphics editor GUI

import math
from tkinter import *

TILES_X = 8
TILES_Y = 8
TILE_WIDTH = 30
OUTLINE_WIDTH = 2

boardTiles = [[0 for i in range(TILES_X)] for j in range(TILES_Y)]
pixelData =[[0]*8 for i in range(8)]
screenModes = ["0", "1"]
charCode = 0x50
charRomStart = 0x1000

colors = [0, 1, 2, 3]

ws = Tk()
ws.title('goOSe Graphics Editor GUI')
#ws.geometry('300x300')
ws.config(bg='#345')

def get_color(code):
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

canvas = Canvas(
    ws,
    height = TILES_Y*TILE_WIDTH+2,
    width = TILES_X*TILE_WIDTH+2,
    bg="#ccc"
    )

def Write_Output(text: Text):
    outStr = ""
    for i in range(8):
        byteVal = 0
        for j in range (8):
            byteVal += (pixelData[i][7-j] << j)
        outStr += ("mov ar " + hex(byteVal).replace("0x", "") + "\n")
        outStr += "mov *" + hex(charRomStart + charCode*8 + i).replace("0x", "") + " ar\n"
    text.config(state='normal')
    text.delete(1.0, END)
    text.insert(1.0, outStr)
    text.config(state='disabled')

def Clear_Drawing():
    for i in range(8):
        for j in range (8):
            pixelData[i][j] = 0
            color = get_color(0)
            canvas.itemconfig(i * 8 + j + 1, fill=color)
    Write_Output(outputText)

def Char_Code_Update(event):
    global charCode
    input = charCodeEntry.get()
    try:
        charCode = int(input, 16)
        #print(hex(charCode))
        Write_Output(outputText)
    except:
        pass

def Char_Rom_Update(event):
    global charRomStart
    input = charRomEntry.get()
    try:
        charRomStart = int(input, 16)
        #print(hex(charCode))
        Write_Output(outputText)
    except:
        pass

def Print_Pixel(tileX, tileY):
    if (int(screenMode.get()) == 0):
        color = get_color(colors[pixelData[tileY][tileX]])
        canvas.itemconfig(tileY * 8 + tileX + 1, fill=color)
    elif (int(screenMode.get()) == 1):
        baseX = tileX - tileX % 2
        color = get_color(colors[pixelData[tileY][baseX] * 2 + pixelData[tileY][baseX+1]])
        canvas.itemconfig(tileY * 8 + baseX + 1, fill=color)
        canvas.itemconfig(tileY * 8 + baseX + 2, fill=color)

def Print_All_Pixels(*args):
    #print("Print all")
    for i in range(8):
        for j in range(8):
            Print_Pixel(j, i)

def Color_Update(event: Event):
    global colors
    input = 0
    colorIndex = 0
    name = str(event.widget).split(".")[-1]
    if (name == "color0entry"):
        colorIndex = 0
        input = color0Entry.get()
    if (name == "color1entry"):
        colorIndex = 1
        input = color1Entry.get()
    if (name == "color2entry"):
        colorIndex = 2
        input = color2Entry.get()
    if (name == "color3entry"):
        colorIndex = 3
        input = color3Entry.get()
    try:
        colors[colorIndex] = int(input, 16)
        #print(hex(charCode))
        Print_All_Pixels()
    except:
        pass

# Draw initial tiles
color = get_color(0)
for i in range(TILES_Y):
    for j in range(TILES_X):
        canvas.create_rectangle(j*TILE_WIDTH+OUTLINE_WIDTH+1,
                                i*TILE_WIDTH+OUTLINE_WIDTH+1,
                                (j+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                (i+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                outline="#666",
                                fill=color,
                                width=OUTLINE_WIDTH)


charCodeEntry = Entry(ws, width = 8, 
              bg = "white")
charCodeEntry.bind('<KeyRelease>', Char_Code_Update)
charCodeEntry.insert(END, hex(charCode).replace("0x", ""))

charCodeLabel = Label(text="Character code: 0x", bg="light cyan")

charRomEntry = Entry(ws, width = 8, 
              bg = "white")
charRomEntry.bind('<KeyRelease>', Char_Rom_Update)
charRomEntry.insert(END, hex(charRomStart).replace("0x", ""))

charRomLabel = Label(text="Character ROM location: 0x", bg="light cyan")

clearBtn = Button(ws, text = 'Clear Drawing', 
                command = Clear_Drawing, bg="orange") 

outputText = Text(ws, height = 16, 
              width = 25, 
              bg = "light cyan")
outputLabel = Label(text="Output", bg="light cyan")

screenMode = StringVar(ws)
screenMode.set(screenModes[0]) # default value

screenModeMenu = OptionMenu(ws, screenMode, *screenModes)
screenModeLabel = Label(text="Screen mode: ", bg="light cyan")

color0Label = Label(text="Color 0 (BG): 0x", bg="light cyan")
color0Entry = Entry(ws, width = 8, bg = "white", name="color0entry")
color0Entry.bind('<KeyRelease>', Color_Update)
color0Entry.insert(END, hex(colors[0]).replace("0x", ""))

color1Label = Label(text="Color 1: 0x", bg="light cyan")
color1Entry = Entry(ws, width = 8, bg = "white", name="color1entry")
color1Entry.bind('<KeyRelease>', Color_Update)
color1Entry.insert(END, hex(colors[1]).replace("0x", ""))

color2Label = Label(text="Color 2: 0x", bg="light cyan")
color2Entry = Entry(ws, width = 8, bg = "white", name="color2entry")
color2Entry.bind('<KeyRelease>', Color_Update)
color2Entry.insert(END, hex(colors[2]).replace("0x", ""))

color3Label = Label(text="Color 3: 0x", bg="light cyan")
color3Entry = Entry(ws, width = 8, bg = "white", name="color3entry")
color3Entry.bind('<KeyRelease>', Color_Update)
color3Entry.insert(END, hex(colors[3]).replace("0x", ""))


canvas.grid(row = 1, column = 0, sticky = W, padx = 5, pady = 2, columnspan=3)
clearBtn.grid(row = 2, column = 0, sticky = W, padx=20, pady = 5)

outputLabel.grid(row = 0, column = 3, sticky = W, padx=20, pady = 5)
outputText.grid(row = 1, column = 3, sticky = W, padx=20, pady = 0, columnspan=2)

charCodeLabel.grid(row = 2, column = 3, sticky = E, padx=0, pady = 10)
charCodeEntry.grid(row = 2, column = 4, sticky = W, padx=0, pady = 10)

charRomLabel.grid(row = 3, column = 3, sticky = E, padx=0, pady = 5)
charRomEntry.grid(row = 3, column = 4, sticky = W, padx=0, pady = 5)

screenModeLabel.grid(row = 2, column = 1, sticky = E, padx=0, pady = 5)
screenModeMenu.grid(row = 2, column = 2, sticky = W, padx=2, pady = 5)
screenMode.trace_add("write", Print_All_Pixels)

color0Label.grid(row = 3, column = 1, sticky = E, padx=0, pady = 5)
color0Entry.grid(row = 3, column = 2, sticky = W, padx=0, pady = 5)

color1Label.grid(row = 4, column = 1, sticky = E, padx=0, pady = 5)
color1Entry.grid(row = 4, column = 2, sticky = W, padx=0, pady = 5)

color2Label.grid(row = 5, column = 1, sticky = E, padx=0, pady = 5)
color2Entry.grid(row = 5, column = 2, sticky = W, padx=0, pady = 5)

color3Label.grid(row = 6, column = 1, sticky = E, padx=0, pady = 5)
color3Entry.grid(row = 6, column = 2, sticky = W, padx=0, pady = 5)

def Paint(tileX, tileY):
    if (int(screenMode.get()) == 0):
        newData = (pixelData[tileY][tileX] + 1) % 2
        pixelData[tileY][tileX] = newData
    elif (int(screenMode.get()) == 1):
        baseX = tileX - tileX % 2
        newData = ((pixelData[tileY][baseX] * 2 + pixelData[tileY][baseX+1]) + 1) % 4
        pixelData[tileY][baseX] = (newData & 0x2) >> 1
        pixelData[tileY][baseX+1] = newData & 0x1
    Print_Pixel(tileX, tileY)
    Write_Output(outputText)

def Erase(tileX, tileY):
    if (int(screenMode.get()) == 0):
        pixelData[tileY][tileX] = 0
    elif (int(screenMode.get()) == 1):
        baseX = tileX - tileX % 2
        pixelData[tileY][baseX] = 0
        pixelData[tileY][baseX+1] = 0
    Print_Pixel(tileX, tileY)
    Write_Output(outputText)

def leftclick(event):
    if (event.x < TILES_X*TILE_WIDTH and event.y < TILES_Y*TILE_WIDTH):
        Paint(math.floor((event.x-2) / TILE_WIDTH),
                math.floor((event.y-2) / TILE_WIDTH))
    #Print_All_Pixels()



def rightclick(event):
    Erase(math.floor((event.x-2) / TILE_WIDTH),
                math.floor((event.y-2) / TILE_WIDTH))

canvas.bind("<Button-1>", leftclick)
canvas.bind("<Button-3>", rightclick)

Write_Output(outputText)
ws.update()
ws.mainloop()