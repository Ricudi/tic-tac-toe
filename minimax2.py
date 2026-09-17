import timeit

from utils import *
import evaluation_function

PLAYER = "O"        #what side does ai play
MAX_DEPTH = 5       #depth of minimax algorithm
ADMISSABLE_DISTANCE = 1 #max distance of admissable moves
INFINITY = 10
MODE = "DEFENSIVE"    #"DEFENSIVE" / "OFFENSIVE"


evaluation_function.INFINITY = INFINITY
evaluation_function.PLAYER = PLAYER

transposition_table = {}    #(d.items, turn): (value, move, depth_searched)

def SwapTurn(t):
    """
    Swaps between "X" and "O", markers for turn
    """
    if t == "X":
        return "O"
    else:
        return "X"
    

    
def Minimax(d:dict, turn, depth = 0, alpha = -INFINITY, beta = INFINITY):
    """
    minimax algorithm \n
    d: dictionary of moves - position:character\n
    turn: whose turn is it\n
    depth: how many turns to compute in advance
    returns best position to play
    """
    global INFINITY, PLAYER, MAX_DEPTH
    global admissable, transposition_table

    ended = False   #if I know the game is lost only after checking for admissable
    if depth==0:
        transposition_table = {}


    #function for automatically caching move with value into transposition table
    def Cache_Move(value, move):
        nonlocal turn, depth
        transposition_table[(frozenset(d.items()), turn)] = (value, move, depth)

    def GetAdmissable(d:dict):
        """
        Marks all tiles within _ tiles of occupied tiles to be checked\n
        d: dictionary of played moves, indexed by their position\n
        x: max distance from played moves for new moves\n
        Occupied tiles are not admissable
        """
        global ADMISSABLE_DISTANCE, MODE

        admissable = []
        is_in_admissable = set()
        nonlocal value, ended

        if MODE == "DEFENSIVE":
            P = ["X"]
        else:
            P = ["X", "O"]

        ###restrict oneself onto opponent's unblocked 3 chains and partially unblocked 4 chains###  -only for speed up
        directions = [(1,0), (1,1), (0,1), (-1,1)]
        for player in P:
            for pos, piece in d.items():
                if piece == player:    #I want to restrict myself only to block the opponent
                    for dir in directions:
                        unblocked = []
                        length = 1
                        x, y = pos
                        while d.get((x+dir[0], y+dir[1])) == player:
                            length += 1
                            x, y = x+dir[0], y+dir[1]
                        if d.get((x+dir[0], y+dir[1]), "nic") == "nic":
                            unblocked.append((x+dir[0], y+dir[1]))
                        x,y = pos
                        while d.get((x-dir[0], y-dir[1])) == player:
                            length +=1
                            x, y = x-dir[0], y-dir[1]
                        if d.get((x-dir[0], y-dir[1]), "nic") == "nic":
                            unblocked.append((x-dir[0], y-dir[1]))

                        #logic behind restriction
                        if (len(unblocked) == 2) and (length == 3):
                            for i in unblocked:
                                if i not in is_in_admissable:
                                    admissable.append(i)
                                    is_in_admissable.add(i)
                        elif (len(unblocked) == 1) and (length == 4):
                            for i in unblocked:
                                if i not in is_in_admissable:
                                    admissable.append(i)
                                    is_in_admissable.add(i)
                        elif (len(unblocked) == 2) and (length == 4):
                            ended == True
                            return [unblocked[0]]   #return any point, the game is lost anyways
                        

        if len(admissable) > 0: #if there are any chains that need to be blocked, block them immidiately
            for i in admissable:
                if i in d.keys():
                    breakpoint
            return admissable
        ###
        
        ###prioritising closer moves by adding them to resolve first###
        for distance in range(1, ADMISSABLE_DISTANCE+1):    
            for coord in d.keys():
                for i in range(-distance, distance +1):
                    for j in range(-distance, distance+1):
                        x = AddVectors2D(coord, (i, j))
                        if (x not in is_in_admissable) and (x not in d.keys()):
                            admissable.append(x)
                            is_in_admissable.add(x)
        return admissable
        ###
    
    #prepare admissable tiles
    admissable = GetAdmissable(d)
    if ended:
        return (value, admissable[0])

    if (frozenset(d.items()), turn) in transposition_table:
        cached_value, cached_move, cached_depth = transposition_table[(frozenset(d.items()), turn)]
        if cached_depth >= MAX_DEPTH - depth:   #if the cache was made deeper than this
            return (cached_value, cached_move)

    #initialise values
    max_value = (-INFINITY, admissable[-1])   #pair (value, position)
    min_value = (INFINITY, admissable[-1])    #pair (value, position)
    #admissable[-1] is random placeholder, that won't be obstructed during first iteration


    ###recursion over all move combinations###
    for move in admissable:
        if move in d.keys():
            continue    #so I can't play already played move
        d[move] = turn

        if max(evaluation_function.LengthOfChain(d, move, turn)) >= 5:
            if turn == PLAYER:
                del d[move]
                return (INFINITY, move)
            else:
                del d[move]
                return  (-INFINITY, move)
        if depth == MAX_DEPTH-1:
            value = evaluation_function.EvaluatePosition(d)
        else:
            value = Minimax(d, SwapTurn(turn), depth+1, alpha, beta)[0]

        del d[move]

        ### evaluating best move###
        if (turn == PLAYER) and (value == INFINITY):
            Cache_Move(value, move)
            return (value, move)
        elif (turn != PLAYER) and (value == -INFINITY):
            Cache_Move(value, move)
            return (value, move)

        if (turn == PLAYER) and (value > max_value[0]):
            max_value = (value, move)
            alpha = max(alpha, value)
        elif (turn != PLAYER) and (value < min_value[0]):
            min_value = (value, move)
            beta = min(beta, value)

        if alpha >= beta: #ořezávání
            break
        ###
    ###
    
    ###return the best move###
    if (turn == PLAYER):
        Cache_Move(0.9 * value, move)
        return (0.9 *max_value[0], max_value[1])
    else:
        Cache_Move(0.9 * value, move)
        return (0.9 * min_value[0], min_value[1]) 
    ####



