# tic-tac-toe
tic-tac-toe on an infinite grid made as a school project
made by Pavel Petrok

This project runs on pygame library

Warning! While it theoretically runs on an infinite grid, it is recommended to play 'normally' in one place.
Spreading your moves too much may result in unreasonably poor performance.

Recomended constants in minimax:
PLAYER = "O"             
#this one probably can't be changed

MAX_DEPTH = 4 or 5
#4 is faster, but 5 leads to smarter AI.
If the game gets too complex, it will freeze and lose all progress. 
This issue occured only during testing with MAX_DEPTH = 5.
Values less than 4 are possible and lead to fast AI, although not very smart.
They are not recommended.

ADMISSABLE DISTANCE = 1  
#since admissable rework, 1 is enough and increasing this 
number probably won't have effect on the AI

MODE = "DEFENSIVE"  / "OFFENSIVE"
#on DEFENSIVE, AI will be forced to defend unblocked threats,
even if AI itself could win sooner. This is the recommended option.
#on OFFENSIVE, AI gets the option to not defend unblocked threats,
however it will often not defend in the wrong position


