import math

def AddVectors2D(x,y):
    """
    adds two pairs elementwise, 
    returns resulting pair
    """
    if len(x) != len(y) and len(x)!=2:
        raise "vektory nejsou 2D"
    z = (x[0]+y[0], x[1]+y[1])
    return z

def SubVectors2D(x,y):
    """
    subtracts two pairs elementwise,
    returns resulting pair
    """
    if len(x) != len(y) and len(x)!=2:
        raise "vektory nejsou 2D"
    z = (x[0]-y[0], x[1]-y[1])
    return z

def MultVector2D(x, k):
    """
    multiplies a pair by a constant elementwise\n
    x: vector, k: constant\n
    returns resulting pair
    """
    z = (k*x[0], k*x[1])
    return z

def GetCoord2D(x, i=64):
    """
    Gets a nearest lower (in both coordinates) gridpoint to the vector X. 
    The grid is square with grid number i (64 if not given)
    """
    z = ((x[0]//i), (x[1]//i))
    return z

def VectorSize(x):
    """
    returns euclidian size of a vector x
    """
    return math.sqrt(sum(a**2 for a in x))