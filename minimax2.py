import timeit

from utils import *
import evaluation_function

PLAYER = "O"        #what side does ai play
MAX_DEPTH = 2       #depth of minimax algorithm
ADMISSABLE_DISTANCE = 1 #max distance of admissable moves
INFINITY = 10

test_iter_value = 0

evaluation_function.INFINITY = INFINITY
evaluation_function.PLAYER = PLAYER

admissable = []
found_positions = set()

def SwapTurn(t):
    """
    Swaps between "X" and "O", markers for turn
    """
    if t == "X":
        return "O"
    else:
        return "X"
    
def GetAdmissable(d:dict):
    """
    Marks all tiles within _ tiles of occupied tiles to be checked\n
    d: dictionary of played moves, indexed by their position\n
    x: max distance from played moves for new moves\n
    Occupied tiles are not admissable
    """
    global ADMISSABLE_DISTANCE
    global admissable

    is_in_admissable = set()

    #prioritising closer moves by adding them to resolve first
    for distance in range(1, ADMISSABLE_DISTANCE+1):    
        for coord in d.keys():
            for i in range(-distance, distance +1):
                for j in range(-distance, distance+1):
                    x = AddVectors2D(coord, (i, j))
                    if x not in is_in_admissable:
                        admissable.append(x)
                        is_in_admissable.add(x)
    
def Minimax(d:dict, turn, depth = 0):
    """
    minimax algorithm \n
    d: dictionary of moves - position:character\n
    turn: whose turn is it\n
    depth: how many turns to compute in advance
    returns best position to play
    """
    global INFINITY, PLAYER, MAX_DEPTH
    global admissable

    global test_iter_value #delete later

    #prepare admissable tiles
    if depth == 0:
        GetAdmissable(d)
    
    #initialise values
    max_value = (-INFINITY, admissable[-1])   #pair (value, position)
    min_value = (INFINITY, admissable[-1])    #pair (value, position)
    #admissable[-1] is random placeholder, that won't be obstructed during first iteration

    ####
    #terminal condition for recursion
    if depth == MAX_DEPTH-1:
        #try all moves
        for move in admissable:
            test_iter_value += 1
            #print(test_iter_value)
            #skip already played positions
            if move in d.keys():
                continue   

            #evaluate moves using evaluation function
            d[move] = turn
            value = evaluation_function.EvaluatePosition(d)
            #return to original state
            del d[move]

            #end algorithm if already found best move
            if (turn == PLAYER) and (value == INFINITY):
                return (value, move)
            elif (turn != PLAYER) and (value == -INFINITY):
                return (value, move)

            #pick the best one
            if (turn == PLAYER) and (value > max_value[0]):
                max_value = (value, move)
            elif (turn != PLAYER) and (value < min_value[0]):
                min_value = (value, move)

        #return the best one
        if (turn == PLAYER):
            return max_value
        else:
            return min_value
    ####

    ####
    #try all possible moves
    for move in admissable:
        test_iter_value += 1
        #print(test_iter_value)
        #skip already played positions
        if move in d.keys():
            continue  
        
        #evaluate moves recursively
        d[move] = turn
        value = Minimax(d, SwapTurn(turn), depth+1)[0]
        #return to original state
        del d[move]
        
        #end algorithm if already found best move
        if (turn == PLAYER) and (value == INFINITY):
            return (value, move)
        elif (turn != PLAYER) and (value == -INFINITY):
            return (value, move)

        #pick the best move
        if (turn == PLAYER) and (value > max_value[0]):
            max_value = (value, move)
        elif (turn != PLAYER) and (value < min_value[0]):
            min_value = (value, move)

    #return the best move
    if (turn == PLAYER):
        return max_value
    else:
        return min_value
    ####
    

test = {
    (3,0):"O",
    (2,0):"O",
    (0,2):"X",
    (0,3):"X",
    (0,4):"X"
}

MAX_DEPTH = 3
ADMISSABLE_DISTANCE = 1
t1 = timeit.default_timer()
print(Minimax(test, "O"))
t2 = timeit.default_timer()
print("time1: ", t2-t1)

MAX_DEPTH = 2
ADMISSABLE_DISTANCE = 3
t1 = timeit.default_timer()
print(Minimax(test, "O"))
t2 = timeit.default_timer()
print("time2: ", t2-t1)

