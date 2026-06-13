from utils import *

INFINITY = 10
PLAYER = "O"
values = {} #dictionary for storing values of all positions

def NormalisationFunction(value):
    """
    normalises value to range (0,10)
    """
    return (10*value)/(value + 12)

def EvaluatePosition(position: dict):
    position_value = 0
    vs= 0
    for move in position.keys():
        #set hard-winning/losing positions (5 in a row = win/lose)
        #5 in a row
        if eval(" and ".join([f"(position.get(AddVectors2D(({-k},0), move), 'empty') == position[move])" for k in range(-4,0)])):
            if position[move] == PLAYER:
                return INFINITY
            else:
                return -INFINITY

        #5 in a column 
        if eval(" and ".join([f"(position.get(AddVectors2D((0,{-k}), move), 'empty') == position[move])" for k in range(-4,0)])):
            if position[move] == PLAYER:
                return INFINITY
            else:
                return -INFINITY
            
        #5 on north-east diagonal
        if eval(" and ".join([f"(position.get(AddVectors2D(({-k},{-k}), move), 'empty') == position[move])" for k in range(-4,0)])):
            if position[move] == PLAYER:
                return INFINITY
            else:
                return -INFINITY
            
        #5 on north-west diagonal
        if eval(" and ".join([f"(position.get(AddVectors2D(({k},{-k}), move), 'empty') == position[move])" for k in range(-4,0)])):
            if position[move] == PLAYER:
                return INFINITY
            else:
                return -INFINITY

        move_value = 0
        #checks how many moves in a row are there
        vs = 0
        for k in range(-4, 0):
            if (position.get(AddVectors2D((k,0), move), "empty") == position[move]):
                vs += 1
        move_value = max(move_value, vs*2)
        
        #checks how many moves in a column are there
        vs = 0
        for k in range(-4, 0):
            if (position.get(AddVectors2D((0,k), move), "empty") == position[move]):
                vs += 1
        move_value = max(move_value, vs*2)
        
        #checks how many moves on a north-east diagonal are there
        vs = 0
        for k in range(-4, 0):
            if (position.get(AddVectors2D((-k,-k), move), "empty") == position[move]):
                vs += 1
        move_value = max(move_value, vs*2)

        #checks how many moves on a north-west diagonal are there
        vs = 0
        for k in range(-4, 0):
            if (position.get(AddVectors2D((k,-k), move), "empty") == position[move]):
                vs += 1
        move_value = max(move_value, vs*2)

        if position[move] == PLAYER:
            position_value += move_value
        else:
            position_value -= move_value
    
    if position_value >= 0:
        return NormalisationFunction(position_value)
    else:
        return -NormalisationFunction(-position_value)


test = {
    (3,0):"O",
    (2,0):"O",
    (0,2):"X",
    (0,3):"X",
    (0,4):"X"
}