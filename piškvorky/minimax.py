import utils
import copy
import evaluation_function

PLAYER = "O"        #what side does ai play
MAX_DEPTH = 2       #depth of minimax algorithm
ADMISSABLE_DISTANCE = 1 #max distance of admissable moves
INFINITY = 10
admissable = set()  #set of tiles to be checked by algorithm

test_iter_value = 0

evaluation_function.INFINITY = INFINITY
evaluation_function.PLAYER = PLAYER

class Choice():
    def __init__(self, value, player, position, successor=None):
        self.value = value          #value of this choice
        self.player = player        #player to make said choice
        self.pos = position         #position of move to make
        self.successor = successor  #bearing value to be acquired

    def __repr__(self):
        return f"hodnota: {self.value}, hráč: {self.player}, pozice: {self.pos}"

def SwapTurn(t):
    """
    Swaps between "X" and "O", markers for turn
    """
    if t == "X":
        return "O"
    else:
        return "X"

def GetAdmissable(d: dict, x=ADMISSABLE_DISTANCE):
    """
    Marks all tiles within _ tiles of occupied tiles to be checked\n
    d: dictionary of played moves, indexed by their position\n
    x: max distance from played moves for new moves\n
    Occupied tiles are not admissable
    """
    #possible improvement to prioritise moves adjecent to moves on the board
    global admissable
    for (_, coord) in enumerate(d.keys()):
        for i in range(-x, x+1):
            for j in range(-x, x+1):
                new_coord = utils.AddVectors2D((i, j), coord)
                if not d.get(new_coord, False):     #if tile in d is empty
                    admissable.add(new_coord)

def Evaluate(d:dict, turn) -> float:
    """
    Evaluates position stored in d\n
    returns float bouded to (-10, 10)\n
    -10 means lose, 10 means win
    """
    global PLAYER, INFINITY
    return evaluation_function.EvaluatePosition(d)
    

def Minimax(d: dict, turn, depth = 0) -> Choice:
    """
    minimax algorithm \n
    d: dictionary of moves - position:character\n
    turn: whose turn is it\n
    depth: how many (PC) turns in advance
    returns best possible Choice
    """
    global PLAYER, MAX_DEPTH, INFINITY
    global admissable
    global test_iter_value  #delete later

    #get admissable tiles
    if depth == 0:
        GetAdmissable(d)

    #terminal condition
    if depth >= MAX_DEPTH-1:    #last move before evaluation
        max_value = (-INFINITY-1, None)
        min_value = (INFINITY+1, None)
        for (_, tile) in list(enumerate(admissable)):
            test_iter_value += 1
            print(test_iter_value)

            #set state
            admissable.remove(tile)
            d[tile] = turn
            
            #evaluate
            v = Evaluate(d, SwapTurn(turn))
            #set max_value
            if turn == PLAYER:
                if v > max_value[0]:
                    max_value = (max(max_value[0], v), tile)
            else:
                if v < min_value[0]:
                    min_value = (min(min_value[0], v), tile)

            #return to previous state
            admissable.add(tile)
            del d[tile]

        #stop when I find max/min
        if (turn == PLAYER) and max_value[0] == INFINITY:
            return Choice(-INFINITY, turn, max_value[1])
        elif (turn != PLAYER) and min_value[0] == -INFINITY:
            return Choice(-INFINITY, turn, min_value[1])

        if turn == PLAYER:
            return Choice(max_value[0], turn, max_value[1])
        else:
            return Choice(min_value[0], turn, min_value[1])

    #go through all possibilities
    max_value = Choice(-INFINITY-1, None, None)
    min_value = Choice(INFINITY+1, None, None)    #placeholders
    for (_, tile) in list(enumerate(admissable)):
        test_iter_value += 1
        print(test_iter_value)

        #set state
        admissable.remove(tile)
        d[tile] = turn

        #score possibility
        c = Choice(Minimax(d, SwapTurn(turn), depth+1).value, turn, tile)

        #return to previous state
        admissable.add(tile)
        del d[tile]

        #set max_value
        if turn == PLAYER:
            if c.value > max_value.value:
                max_value = c
            if max_value.value == INFINITY:
                return max_value
        else:
            if c.value < min_value.value:
                min_value = c
            if min_value.value == -INFINITY:
                return min_value

    #choose biggest score
    if turn == PLAYER:
        return max_value
    else:
        return min_value
    
test = {
    (0,-1):"O",
    (0,-2):"O",
    (0,-3):"O",
    (0,-4):"O"
}

#print(Minimax(test, "O"))