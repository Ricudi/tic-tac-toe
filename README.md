# tic-tac-toe
tic-tac-toe on an infinite grid made as a school project
made by Pavel Petrok

This project runs on pygame library

Recomended constants:
PLAYER = "O"             
#this one probably can't be changed

MAX_DEPTH = 4 or 5
#4 is faster, but 5 leads to smarter AI.
If the game gets too complex, it will freeze and lose all progress. 
This issue occured only during testing MAX_DEPTH = 5

ADMISSABLE DISTANCE = 1  
#since admissable rework, 1 is enough and increasing this 
number probably won't have effect on the AI

MODE = "DEFENSIVE"
on DEFENSIVE, AI will be forced to defend unblocked threats,
even if AI itself could win sooner. This is the recommended option.
on OFFENSIVE, AI gets the option to not defend unblocked threats,
however it will often not defend in the wrong position


