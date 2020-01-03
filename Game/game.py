import board as bd
import player as pl
import numpy as np


class Game:
    def __init__(self):
        self._board = bd.Board()
    
    def getBoard(self):
        return self._board


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

    def _getAvailablePathMovement(self,square,player):
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
            if (player.getColor() == pl.Player.RED):
                if (color == bd.Pawns.BLUE or color ==bd.Pawns.BLUE_KING): #not using his pawn
                    raise bd.PawnsException("It is not your pawn !")
            else :
                if (color == bd.Pawns.RED or color == bd.Pawns.RED_KING): #not using his pawn
                    raise bd.PawnsException("It is not your pawn !")
            
            if (color == bd.Pawns.BLUE or color == bd.Pawns.RED): #for simple pawn

                self._checkSimplePawnsMovement(x,y,player.getColor(),self._board,paths)

                if (len(paths) == 0): #we have an obligatory movement
                    obligatory = False
                    if (player.getColor() == pl.Player.BLUE):
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
                self._checkKingPawnsMovement(x,y,player.getColor(),self._board,paths)
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

    def getAvailableMovementForAllPawns(self,player):
        '''
            Return a list of all available movement for all pawns
        '''
        if (player.getColor() == pl.Player.RED):
            myPawn = [bd.Pawns.RED, bd.Pawns.RED_KING]
        else:
            myPawn = [bd.Pawns.BLUE, bd.Pawns.BLUE_KING]

        movements = []
        obligatoryMovementFounded = False #if there are obligatories movement that the player must to do
        for x in range (self._board.SIZE_X):
            for y in range(self._board.SIZE_Y):
                try:
                    if (self._board.getSquare(x,y) in myPawn):
                        obligatory,movementPawn = self._getAvailablePathMovement((x,y),player)
                        
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

        return movements

if __name__ == "__main__":
    g=Game()
    g.getBoard().display()
    #print(b.getSquare(2,2))

    p = pl.Player(pl.Player.RED,True)
    #g.getAvailablePathMovement((0,2),p) #not your pawn
    #g.getAvailablePathMovement((0,5),p) #square not valid
    #print(g.getAvailablePathMovement((0,6),p)) #nothing there is always a pawn in (1,5)
    #print(g.getAvailablePathMovement((1,5),p))
    #print(g.getAvailablePathMovement((7,5),p)) 

    p = pl.Player(pl.Player.BLUE,True) #blue
    #print(g.getAvailablePathMovement((0,0),p)) #nothing there is always a pawn in (1,5)
    #print(g.getAvailablePathMovement((2,2),p)) 
    #print(g.getAvailablePathMovement((0,2),p)) 
    g._board.setSquare(1,3,bd.Pawns.RED)
    g._board.display()
    print(g._getAvailablePathMovement((2,2),p)) 

    g._board.setSquare(2,6,bd.Pawns.NULL)
    g._board.display()
    print(g._getAvailablePathMovement((2,2),p))

    p = pl.Player(pl.Player.RED,True) #blue
    g._board.reset()
    g._board.setSquare(2,4,bd.Pawns.BLUE)
    g._board.display()
    print(g._getAvailablePathMovement((3,5),p)) 

    g._board.setSquare(3,1,bd.Pawns.NULL)
    g._board.display()
    print(g._getAvailablePathMovement((3,5),p))

    p = pl.Player(pl.Player.BLUE,True) #blue
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
    print(g.getAvailableMovementForAllPawns(p))
    print(g2.getAvailableMovementForAllPawns(p))







