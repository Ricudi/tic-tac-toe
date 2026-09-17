import pygame as pg
from utils import *
from sys import exit
#import minimax
import minimax2

moves = []      #list of played moves for rendering
moves_dict = {} #dictionary for played moves; position:character
turn = "X"

def DrawGrid(color):
    """
    color is background color for the grid
    returns surface with grid drawn on top of it
    """
    #initialise surface
    surface = pg.Surface((1000,1000))
    surface.fill(color)
    
    sliceX = 64
    sliceY = 64
    #vertical lines
    for i in range(round(1000/64)+1):
        pg.draw.line(surface, "black", (i*sliceX, 0), (i*sliceX, 1000), 1)
    #horizontal lines
    for j in range(round(1000/64)+1):
        pg.draw.line(surface, "black", (0, j*sliceY), (1000, j*sliceY), 1)
    return surface

def SwapTurn(char):
    if char == "X":
        return "O"
    else:
        return "X"
    

class TestImage():
    def __init__(self, pos):
        self.dot = self.CreateDot()
        self.O = self.CreateChar("O")
        self.X = self.CreateChar("X")
        self.pos = pos
        self.pos_x = pos[0]
        self.pos_y = pos[1]
    def CreateDot(self):
        surface = pg.Surface((10,10))
        surface.fill((0, 0, 0, 0))  #transparent color
        rect = surface.get_rect()
        pg.draw.circle(surface, "green", rect.center, 5)
        return surface
    def CreateChar( self, char):
        if char == "O":
            return pg.image.load("piškvorky\images\O.png")
        else:
            return pg.image.load("piškvorky\images\X.png")
        
class Move():
    def __init__(self, char, pos):
        self.char = char
        self.surface = self.CreateChar(char)
        self.pos = pos      #stored in grid coordinates
    def CreateChar(self, char):
        if char == "O":
            return pg.image.load("piškvorky\images\O.png")
        else:
            return pg.image.load("piškvorky\images\X.png")

def CheckWin(player) -> bool:
    directions = [(1,0), (1,1), (0,1), (-1,1)]
    x0, y0 = moves[-1].pos

    
    for d in directions:
        x,y = x0+d[0], y0+d[1]    #x, y coordinates of currently  probed position
        length = 1 #length of successive moves from player
        while moves_dict.get((x, y)) == player:
            x,y = x+d[0], y+d[1] #set to look at different position
            length += 1
        x,y = x0-d[0], y0-d[1]
        while moves_dict.get((x,y)) == player:
            x,y = x-d[0], y-d[1]
            length += 1
        if length >= 5:
            return True #if there are more than 5 from the same player in a row
    return False    #if there aren't 5 in a row in any direction


def Main():
    global turn, moves, moves_dict

    running = True
    pg.display.init()
    surface = pg.display.set_mode((800,600))
    offset = (0,0)
    base_pos = (400,300)    #middle of the screen on load
    position = base_pos     #initialise position
    mouse_down = False

    while running:

        #enemy AI
        if (turn == "O"):
            AIChoice = (minimax2.Minimax(moves_dict, turn))
            AIMove = Move("O", AIChoice[1])
            moves.append(AIMove)
            moves_dict[AIMove.pos] = AIMove.char
            if CheckWin(turn):
                print("AI vyhralo")
                running = False
            turn = SwapTurn(turn)


        #draw grid
        grid = DrawGrid((100,0,0,0))    #this should be transparent, but it renders alpha value wrong, so instead it's
                                        #set to this random non-opaque color as background
                                        #because of this, all objects on screen to be rendered below this point
        surface.blit(grid, AddVectors2D((position[0]%64,position[1]%64), (-128, -128)))   #added offset, so edges can't be seen on the screen


        #inputs
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            running = False
        
        #events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_down = True

            if event.type == pg.MOUSEBUTTONUP:
                mouse_down = False

                #place moves
                if VectorSize(offset) <= 10:
                    #position of a click on the grid
                    click_pos = GetCoord2D(SubVectors2D(pg.mouse.get_pos(), position))  
                    #mirror along both axes, because inputs are flipped in pygame
                    click_pos = MultVector2D(click_pos, -1)
                    if click_pos not in moves_dict: #only one move in one space
                        t = Move(turn, click_pos)
                        moves.append(t)
                        moves_dict[click_pos] = t.char
                        if CheckWin(turn):
                            print("Vyhrál jsi")
                            running = False
                        turn = SwapTurn(turn) 

                #reset position
                base_pos = position
                offset = (0,0)

        #---render moves---
        for i in moves:   
            surface.blit(i.surface, SubVectors2D(position, MultVector2D(i.pos, 64)))

        #---preparations for next frame---
        #calculate offset
        diff = pg.mouse.get_rel()   #chci zavolat get_rel() každý frame
        #move around
        if mouse_down:
            offset = AddVectors2D(diff, offset)
            position = AddVectors2D(offset, base_pos)
        pg.display.update()

pg.init()
if input("type 'Y' if AI should start ").lower() == "y":
    #enemy AI start
    AIChoice = (0,(0,0))
    AIMove = Move("O", AIChoice[1])
    moves.append(AIMove)
    moves_dict[AIMove.pos] = AIMove.char
turn = "X"
Main()
pg.quit()