

def Wrapper(d:dict):
    value = 0
    ended = False

    def GetAdmissable(d:dict):
        """
        Marks all tiles within _ tiles of occupied tiles to be checked\n
        d: dictionary of played moves, indexed by their position\n
        x: max distance from played moves for new moves\n
        Occupied tiles are not admissable
        """
        global ADMISSABLE_DISTANCE

        admissable = []
        is_in_admissable = set()
        nonlocal value, ended

        ###restrict oneself onto opponent's unblocked 3 chains and partially unblocked 4 chains###  -only for speed up
        directions = [(1,0), (1,1), (0,1), (-1,1)]
        for player in ["X"]:
            for pos, piece in d.items():
                if piece == "X":    #I want to restrict myself only to block the opponent
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
    return GetAdmissable(d)

board = {(1, 0): 'X', (0, -1): 'O', (0, 1): 'X', (0, 0): 'O', (-1, 2): 'X', (-2, 3): 'O', (-1, 0): 'X', (0, -2): 'O', (1, 2): 'X'}
print(Wrapper(board))