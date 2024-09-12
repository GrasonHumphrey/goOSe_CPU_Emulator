# Minesweeper
# Started 5/8/23

import math
import random
from tkinter import *
import time
import sys

sys.setrecursionlimit(10000)

TILES_X = 10
TILES_Y = 10
TILE_WIDTH = 30
OUTLINE_WIDTH = 2

STARTING_MINES = (int)((TILES_X*TILES_Y)/5)

possibleTiles = list()
boardTiles = [[0 for i in range(TILES_X)] for j in range(TILES_Y)]

boardSet=False
gameOver=False
correctTiles=0

ws = Tk()
ws.title('Minesweeper')
#ws.geometry('300x300')
ws.config(bg='#345')

canvas = Canvas(
    ws,
    height = TILES_Y*TILE_WIDTH+2,
    width = TILES_X*TILE_WIDTH+2,
    bg="#fff"
    )

# Draw initial tiles
for i in range(TILES_X):
    for j in range(TILES_Y):
        possibleTiles.append([i,j])
        canvas.create_rectangle(i*TILE_WIDTH+OUTLINE_WIDTH+1,
                                j*TILE_WIDTH+OUTLINE_WIDTH+1,
                                (i+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                (j+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                outline="#666",
                                fill="#bbb",
                                width=OUTLINE_WIDTH)


canvas.pack()

def updateSquares():
    for i in range(TILES_X):
        for j in range(TILES_Y):
            if(boardTiles[j][i] == -2):
                canvas.create_rectangle(i*TILE_WIDTH+OUTLINE_WIDTH+1,
                                j*TILE_WIDTH+OUTLINE_WIDTH+1,
                                (i+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                (j+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                outline="#666",
                                fill="#eee",
                                width=OUTLINE_WIDTH)

def reveal(tileX, tileY):
    global boardSet
    global boardTiles
    global gameOver
    global correctTiles
    adjMines=0
    #print("left")
    #print([tileX, tileY])
    if not boardSet:
        boardSet=True
        #print(possibleTiles)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                try:
                    possibleTiles.remove([max(min(tileX+i, TILES_X-1), 0),
                                      max(min(tileY+j, TILES_Y-1), 0)])
                except:
                    pass

        #print(possibleTiles)
        random.shuffle(possibleTiles)
        for i in range(STARTING_MINES):
            randTile = possibleTiles.pop()
            boardTiles[randTile[1]][randTile[0]] = -1
        #print (boardTiles)
        updateSquares()
    if boardTiles[tileY][tileX] == -1:
        canvas.create_text(180,
                           45,
                           font=('Helvetica','25','bold'),
                           text="Game Over")
        gameOver=True
        canvas.create_rectangle(tileX*TILE_WIDTH+OUTLINE_WIDTH+1,
                                tileY*TILE_WIDTH+OUTLINE_WIDTH+1,
                                (tileX+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                (tileY+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                outline="#666",
                                fill="#b00",
                                width=OUTLINE_WIDTH)
        return
    elif boardTiles[tileY][tileX] == 0:
        correctTiles += 1
        canvas.create_rectangle(tileX*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    tileY*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    (tileX+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    (tileY+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    outline="#666",
                                    fill="#eee",
                                    width=OUTLINE_WIDTH)

        if correctTiles >= (TILES_X*TILES_Y-STARTING_MINES):
            gameOver=True
            canvas.create_text(180,
                           45,
                           font=('Helvetica','25','bold'),
                           text="You Win!!")

        # -2 means the tile is revealed
        boardTiles[tileY][tileX] = -2
        
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (tileX+i >= 0) and (tileX+i < TILES_X) and (tileY+j >= 0) and (tileY+j < TILES_Y):
                    if boardTiles[tileY+j][tileX+i] == -1 or boardTiles[tileY+j][tileX+i] == -4:
                        adjMines += 1
        #print(adjMines)
        if(adjMines > 0):
            canvas.create_text(tileX*TILE_WIDTH+TILE_WIDTH/2+2,
                               tileY*TILE_WIDTH+TILE_WIDTH/2+2,
                               font=('Helvetica','18','bold'),
                               text=str(adjMines))
        else:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if not ((i==0) and (j==0)):
                        if (tileX+i >= 0) and (tileX+i < TILES_X) and (tileY+j >= 0) and (tileY+j < TILES_Y):
                            if not boardTiles[tileY+j][tileX+i] == -2:
                                reveal(tileX+i, tileY+j)

def leftclick(event):
    if not gameOver:
        reveal(math.floor((event.x-2) / TILE_WIDTH),
               math.floor((event.y-2) / TILE_WIDTH))


def rightclick(event):
    if not gameOver:
        tileX = math.floor((event.x-2) / TILE_WIDTH)
        tileY = math.floor((event.y-2) / TILE_WIDTH)
        # -3 and -4 means the tile is marked green
        if boardTiles[tileY][tileX] == 0 or boardTiles[tileY][tileX] == -1:
            boardTiles[tileY][tileX] -= 3
            canvas.create_rectangle(tileX*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    tileY*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    (tileX+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    (tileY+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    outline="#666",
                                    fill="#0b0",
                                    width=OUTLINE_WIDTH)
        elif boardTiles[tileY][tileX] == -3 or boardTiles[tileY][tileX] == -4:
            boardTiles[tileY][tileX] += 3
            canvas.create_rectangle(tileX*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    tileY*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    (tileX+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    (tileY+1)*TILE_WIDTH+OUTLINE_WIDTH+1,
                                    outline="#666",
                                    fill="#bbb",
                                    width=OUTLINE_WIDTH)

canvas.bind("<Button-1>", leftclick)
canvas.bind("<Button-3>", rightclick)

ws.update()
ws.mainloop()
