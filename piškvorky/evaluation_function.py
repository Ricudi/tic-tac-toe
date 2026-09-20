from utils import *
from functools import cache

INFINITY = 10
PLAYER = "O"
values = {} #dictionary for storing values of all positions

def SwapTurn(player):
    if player == "X":
        return "O"
    else:
        return "X"

def NormalisationFunction(value):
    """
    normalises value to range (0,10)
    """
    return (10*value)/(value + 12)

def LengthOfChain(board, last_move_position, player):
    """checks how many moves by the same player are in a row for each direction
        returns a list, where each entry corresponds to length in each direction;
        0: up/down, 1: right-up diagonal, 2:left/right, 3:right-down diagonal"""
    L =[]

    directions = [(1,0), (1,1), (0,1), (-1,1)]
    x0, y0 = last_move_position
    
    for d in directions:
        x,y = x0+d[0], y0+d[1]    #x, y coordinates of currently  probed position
        length = 1 #length of successive moves from player
        while board.get((x, y)) == player:
            x,y = x+d[0], y+d[1] #set to look at different position
            length += 1
        x,y = x0-d[0], y0-d[1]
        while board.get((x,y)) == player:
            x,y = x-d[0], y-d[1]
            length += 1
        L.append(length)
    return L

def EvaluatePosition(board: dict, player = "O"):
    best_player_chain = 0
    best_opponent_chain = 0

    for pos, piece in board.items():
        chains = LengthOfChain(board, pos, piece)
        if piece == player:
            best_player_chain = max(best_player_chain, max(chains))
        else:
            best_opponent_chain = max(best_opponent_chain, max(chains))

    if best_player_chain >= 5:
        return INFINITY
    if best_opponent_chain >= 5:
        return -INFINITY

    return NormalisationFunction(best_player_chain) - NormalisationFunction(best_opponent_chain)



test = {
    (3,0):"O",
    (2,0):"O",
    (0,2):"X",
    (0,3):"X",
    (0,4):"X",
    (0,5):"X",
    (0,6):"O"
}

#print(EvaluatePosition(test, (0,5), "X"))
#print(EvaluatePosition(test, (0,5)))