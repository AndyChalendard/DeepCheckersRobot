import board as bd
import player as pl
import numpy as np


class Game:
    def __init__(self,random=False, nbMaxPawnRandom=None):
        self._board = bd.Board()
        self._randomBoard = random
        self._nbMaxPawnRandom = nbMaxPawnRandom
        self.reset()

    def getBoard(self, color):
        '''
        Get the board of the game
        if the color if blue we reverse the board
        '''
        if (color == pl.Player.RED):
            return self._board.copy()
        else:
            return self._board.reverseBoard()

    def isFinished(self,playerColor):
        '''
        Return True if the game is finished
        '''
        red = False #if there are red pawns in the board
        blue = False #if there are blue pawns in the board

        red_pawns = [bd.Pawns.RED, bd.Pawns.RED_KING]
        blue_pawns = [bd.Pawns.BLUE_KING, bd.Pawns.BLUE]

        if (playerColor == pl.Player.RED):
            availableMov= self.getAvailableMovementForAllPawns(pl.Player.RED)
        else:
            availableMov= self.getAvailableMovementForAllPawns(pl.Player.BLUE)
        if (len(availableMov) == 0): #there are only one pawn but it can't be played
            return True

        for x in range(self._board.SIZE_X):
            for y in range(self._board.SIZE_Y):
                try:
                    pawn = self._board.getSquare(x,y)
                    if (pawn in red_pawns ):
                        red = True
                        if (blue):
                            return False
                    elif(pawn in blue_pawns ):
                        blue = True
                        if (red):
                            return False
                except bd.SquareNotValid :
                    pass

        return True

    def reset(self):
        '''
        Reset the game board
        '''
        if (self._randomBoard == False):
            self._board.reset()
        else:
            self._board.randomBoard(self._nbMaxPawnRandom)

    def setMovement(self,pawn,playerColor,movementValid):
        '''
        Method to set a movement in the board
        '''
        score = 0
        goToKing = False
        destination = movementValid[len(movementValid) - 1]
        
        # Convert coordinate for blue player
        if (playerColor == pl.Player.BLUE):
            newMovementValid = []
            for elt in movementValid:
                newMovementValid.append((self._board.SIZE_X - elt[0] - 1,self._board.SIZE_Y - elt[1] - 1))
            movementValid = newMovementValid
            destination = (self._board.SIZE_X - destination[0] - 1,self._board.SIZE_Y - destination[1] - 1)
            pawn = (self._board.SIZE_X - pawn[0] - 1,self._board.SIZE_Y - pawn[1] - 1)

        if (destination[1] == bd.Board.SIZE_Y-1 and playerColor == pl.Player.BLUE ): #the pawn turns into a king
            self._board.setSquare(destination[0],destination[1],bd.Pawns.BLUE_KING)
            if (self._board.getSquare(pawn[0], pawn[1]) == bd.Pawns.BLUE):
                score += 2 # turns into king give 2 points
                goToKing = True
        elif(destination[1] == 0 and playerColor == pl.Player.RED): #the pawn turns into a king
            self._board.setSquare(destination[0],destination[1],bd.Pawns.RED_KING)
            if (self._board.getSquare(pawn[0], pawn[1]) == bd.Pawns.RED):
                score += 2 # turns into king give 2 points
                goToKing = True
        else:
            self._board.setSquare(destination[0],destination[1],self._board.getSquare(pawn[0],pawn[1]))

        self._board.setSquare(pawn[0],pawn[1],bd.Pawns.NULL) #the pawn done a movement

        pawnJumped = [] #list of opponent pawns that the movement jumped
        prec = pawn
        for elt in movementValid:
            if(prec[0] - elt[0] >0): #choose the direction of the movement
                xdir = -1
            else:
                xdir = 1
            if(prec[1] - elt[1] >0):
                ydir = -1
            else:
                ydir = 1
            prec = (prec[0] + xdir,prec[1] + ydir)

            while (prec != elt):
                if(self._board.getSquare(prec[0],prec[1]) != bd.Pawns.NULL):
                    self._board.setSquare(prec[0],prec[1],bd.Pawns.NULL) #there are no opponent pawns here now
                    pawnJumped.append(prec)
                    score += 1 # Jump a pawn give 1 point
                prec = (prec[0] + xdir,prec[1] + ydir)

        return pawnJumped, score, goToKing


    def _checkSimplePawnsMovement(self,x,y,color,board,paths,currentPath = []):
        '''
            Movements obligatory if we jump a pawn
            check if we have obligatories movement to do (if we must kill a pawn)
        '''
        if (color == pl.Player.RED): #get opponent pawns
            pawnOpponent = [bd.Pawns.BLUE_KING, bd.Pawns.BLUE]
        else:
            pawnOpponent = [bd.Pawns.RED_KING, bd.Pawns.RED]

        mouvementAvailable = False

        for i in [-1,1]: #check all positions arround the square
            for j in [-1,1]:
                try: #if the square is in the board
                    if (board.getSquare(x+i,y+j) in pawnOpponent):
                        if (board.getSquare(x+i*2,y+j*2) == bd.Pawns.NULL):
                            mouvementAvailable = True

                            tmpBoard = board.copy()
                            tmpBoard.setSquare(x+i,y+j, bd.Pawns.NULL)

                            tmpPath = currentPath[:]
                            tmpPath.append((x+i*2,y+j*2))

                            self._checkSimplePawnsMovement(x+i*2, y+j*2, color, tmpBoard, paths, tmpPath)
                except bd.SquareNotValid:
                    pass

        if (mouvementAvailable==False) : #there are no pawns to jump with
            if (len(currentPath) != 0) :
                paths.append(currentPath)

    def _checkKingPawnsMovement(self,x,y,color,board,paths,currentPath = []):
        '''
            Movements obligatory if we jump a pawn
            check if we have obligatories movement to do (if we must kill a pawn)
        '''
        if (color == pl.Player.RED): #get opponent pawns
            pawnOpponent = [bd.Pawns.BLUE_KING, bd.Pawns.BLUE]
            myPawn = bd.Pawns.RED
        else:
            pawnOpponent = [bd.Pawns.RED_KING, bd.Pawns.RED]
            myPawn = bd.Pawns.BLUE

        mouvementAvailable = False

        for i in [-1,1]: #check all positions arround the square
            for j in [-1,1]:
                d=1
                try :
                    while (board.getSquare(x+i*d,y+j*d) == bd.Pawns.NULL):
                        d+=1
                    if (board.getSquare(x+i*d,y+j*d) in pawnOpponent):
                        tmpBoard = board.copy()
                        tmpBoard.setSquare(x+i*d,y+j*d, myPawn)

                        d+=1
                        while (board.getSquare(x+i*d,y+j*d) == bd.Pawns.NULL):
                            mouvementAvailable = True

                            tmpPath = currentPath[:]
                            tmpPath.append((x+i*d,y+j*d))

                            self._checkKingPawnsMovement(x+i*d, y+j*d, color, tmpBoard, paths, tmpPath)
                            d+=1
                except bd.SquareNotValid:
                    pass

        if (mouvementAvailable==False) : #there are no pawns to jump with
            if (len(currentPath) != 0) :
                paths.append(currentPath)

    def _getAvailablePathMovement(self,square,playerColor):
        '''
            Return a boolean oblogatory which determine if we have an obligatory movement to do
             a list of different square which if the steps to arrive in an available movement
             - the first tuple in this list is the square
             [[(square),(step1),(step2)],[(square),(step)]]
        '''
        x = square[0]
        y = square[1]
        color = self._board.getSquare(x,y)
        obligatory = True #we have an obligatory movement
        paths = []
        if (color == bd.Pawns.NULL) : #square empty
            raise bd.PawnsException("The square (" + str(x) +"," +str(y) +") don't have any Pawns here")
        else :
            if (playerColor == pl.Player.RED):
                if (color == bd.Pawns.BLUE or color ==bd.Pawns.BLUE_KING): #not using his pawn
                    raise bd.PawnsException("It is not your pawn !")
            else :
                if (color == bd.Pawns.RED or color == bd.Pawns.RED_KING): #not using his pawn
                    raise bd.PawnsException("It is not your pawn !")

            if (color == bd.Pawns.BLUE or color == bd.Pawns.RED): #for simple pawn

                self._checkSimplePawnsMovement(x,y,playerColor,self._board,paths)

                if (len(paths) == 0): #we have an obligatory movement
                    obligatory = False
                    if (playerColor == pl.Player.BLUE):
                        j=1 #the simple pawn can only go ahead
                    else:
                        j=-1#the simple pawn can only go ahead

                    for i in [-1,1]:
                        try: #if the square wanted is in the board
                            if (self._board.getSquare(x+i,y+j) == bd.Pawns.NULL):
                                paths.append([(x+i,y+j)])
                        except bd.SquareNotValid:
                            pass

            else: #for kings
                self._checkKingPawnsMovement(x,y,playerColor,self._board,paths)
                if (len(paths) == 0): #we have an obligatory movement
                    obligatory = False

                    for i in [-1,1]:
                        for j in [-1,1]:
                            try: #if the square wanted is in the board
                                d=1
                                while (self._board.getSquare(x+i*d,y+j*d) == bd.Pawns.NULL):
                                    paths.append([(x+i*d,y+j*d)])
                                    d+=1
                            except bd.SquareNotValid:
                                pass

        if (obligatory==True): #on mange des pions
            max=0
            newPath=[]
            for i in range(len(paths)):
                if (max<len(paths[i])):
                    max = len(paths[i])

            for i in range(len(paths)):
                if (len(paths[i]) == max):
                    newPath.append(paths[i])
            paths=newPath

        for i in range(len(paths)):
            paths[i].insert(0,square)

        return obligatory,paths

    def getAvailableMovementForAllPawns(self,playerColor):
        '''
            Return a list of all available movement for all pawns
        '''
        if (playerColor == pl.Player.RED):
            myPawn = [bd.Pawns.RED, bd.Pawns.RED_KING]
        else:
            myPawn = [bd.Pawns.BLUE, bd.Pawns.BLUE_KING]

        movements = []
        obligatoryMovementFounded = False #if there are obligatories movement that the player must to do
        for x in range (self._board.SIZE_X):
            for y in range(self._board.SIZE_Y):
                try:
                    if (self._board.getSquare(x,y) in myPawn):
                        obligatory,movementPawn = self._getAvailablePathMovement((x,y),playerColor)

                        if (obligatory==True and obligatoryMovementFounded==False):#there are one obligatory movement
                            obligatoryMovementFounded = True
                            movements=[]

                        if (obligatory == obligatoryMovementFounded):
                            for i in range(len(movementPawn)):
                                movements.append(movementPawn[i])

                except bd.SquareNotValid:
                    pass

        max = 0
        for i in range(len(movements)):
            if (max<len(movements[i])):
                max = len(movements[i])

        newMov = []
        for i in range(len(movements)):
            if (max == len(movements[i])):
                newMov.append(movements[i])
        movements = newMov

        if (playerColor == pl.Player.RED):
            return movements
        else:
            reverseMovements = []
            for mov in movements:
                newMov = []
                for elt in mov:
                    newMov.append((self._board.SIZE_X - elt[0] - 1,self._board.SIZE_Y - elt[1] - 1))
                reverseMovements.append(newMov)
            return reverseMovements


    def pawnsCanBePlayed(self,availableMovements):
        '''
        Return a list of pawns that can be played with some movements
        '''
        pawns = []
        for elt in availableMovements:
            if (elt[0] not in pawns):
                pawns.append(elt[0])
        return pawns

    def movementsValid(self,pawn,availableMovements):
        '''
        Return a list of valid movements with a pawn and a list of availablemovements given
        '''
        movements=[]
        for elt in availableMovements:
            if (elt[0] == pawn):
                movements.append(elt[1:])
        return movements


    def getFinalMovement(self, validMovements):
        '''
        Return the final movement, ie. the square of the movement
        '''
        finalMovement = []
        for elt in validMovements:
            finalMovement.append(elt[len(elt)-1])
        return finalMovement

if __name__ == "__main__":
    g=Game()
    #g.getBoard().display()
    #print(b.getSquare(2,2))

    p = pl.Player(pl.Player.RED,pl.PlayerType.HUMAN_TERMINAL)
    #g.getAvailablePathMovement((0,2),p) #not your pawn
    #g.getAvailablePathMovement((0,5),p) #square not valid
    #print(g.getAvailablePathMovement((0,6),p)) #nothing there is always a pawn in (1,5)
    #print(g.getAvailablePathMovement((1,5),p))
    #print(g.getAvailablePathMovement((7,5),p))

    p = pl.Player(pl.Player.BLUE,pl.PlayerType.HUMAN_TERMINAL) #blue
    #print(g.getAvailablePathMovement((0,0),p)) #nothing there is always a pawn in (1,5)
    #print(g.getAvailablePathMovement((2,2),p))
    #print(g.getAvailablePathMovement((0,2),p))
    g._board.setSquare(1,3,bd.Pawns.RED)
    g._board.display()
    print(g._getAvailablePathMovement((2,2),p))

    g._board.setSquare(2,6,bd.Pawns.NULL)
    g._board.display()
    print(g._getAvailablePathMovement((2,2),p))

    p = pl.Player(pl.Player.RED,pl.PlayerType.HUMAN_TERMINAL) #blue
    g._board.reset()
    g._board.setSquare(2,4,bd.Pawns.BLUE)
    g._board.display()
    print(g._getAvailablePathMovement((3,5),p))

    g._board.setSquare(3,1,bd.Pawns.NULL)
    g._board.display()
    print(g._getAvailablePathMovement((3,5),p))

    p = pl.Player(pl.Player.BLUE,pl.PlayerType.HUMAN_TERMINAL) #blue
    g2=Game()
    g2._board.resetEmpty()
    g2._board.setSquare(2,4,bd.Pawns.BLUE_KING)
    g2._board.setSquare(3,3,bd.Pawns.RED)
    g2._board.setSquare(1,5,bd.Pawns.RED)
    g2._board.setSquare(5,1,bd.Pawns.BLUE)
    g2._board.display()
    print(g2._getAvailablePathMovement((2,4),p))
    #g2._board.setSquare(5,3,bd.Pawns.RED)
    g2._board.display()
    print(g2._getAvailablePathMovement((2,4),p))
    #g2._board.setSquare(3,1,bd.Pawns.RED_KING)
    g2._board.display()
    print(g2._getAvailablePathMovement((2,4),p))

    g._board.reset()
    availableMovements = g.getAvailableMovementForAllPawns(p)
    print(availableMovements)
    movementsValid = g.movementsValid((2,2),availableMovements)
    t=[movementsValid[i][-1:] for i in range (len(movementsValid))]
    print(t)





    print(g2.getAvailableMovementForAllPawns(p))

    g3=Game()
    g3._board.resetEmpty()
    g3._board.setSquare(2,4,bd.Pawns.BLUE_KING)
    g3._board.setSquare(5,1,bd.Pawns.BLUE)
    g3._board.display()
    print(g3.isFinished())
