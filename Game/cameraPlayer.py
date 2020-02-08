import imageProcessing as imp
import board as bd
import player as pl
import time
class CameraPlayer:
    '''
    Real player capture by camera
    '''

    def __init__(self):
        self._camera = imp.Camera()
        self._movement = []

    def _getBoardWithMovement(self, board, mvt):
        '''
        return a board with applyied movement
        '''

        board = board.copy()

        pawn = (mvt[0][0],mvt[0][1])
        destination = (mvt[len(mvt)-1][0], mvt[len(mvt)-1][1])
        board.setSquare(destination[0],destination[1], board.getSquare(pawn[0],pawn[1]))
        board.setSquare(pawn[0],pawn[1],bd.Pawns.NULL) #the pawn done a movement

        mvt = mvt[1:] #we delete the pawn
        prec = pawn
        for elt in mvt:
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
                if(board.getSquare(prec[0],prec[1]) != bd.Pawns.NULL):
                    board.setSquare(prec[0],prec[1],bd.Pawns.NULL) #there are no opponent pawns here now
                prec = (prec[0] + xdir,prec[1] + ydir)

        return board

    def _compareBoard(self, estimatedBoard, captureBoard):
        '''
        Compare the two board and return true if the pawn is the same
        pawn is considere the same if they are in the same color
        '''

        for x in range (estimatedBoard.SIZE_X):
            for y in range (estimatedBoard.SIZE_Y):
                try:
                    pawn = estimatedBoard.getSquare(x,y)
                    if (pawn == bd.Pawns.RED_KING):
                        pawn = bd.Pawns.RED
                    elif (pawn == bd.Pawns.BLUE_KING):
                        pawn = bd.Pawns.BLUE
                    
                    if (pawn != captureBoard.getSquare(x,y)):
                        return False
                except bd.SquareNotValid:
                    pass

        return True

    def _getPawnPlayed(self, captureBoard, board, playerColor):
        '''
        Compare two board and return the pawn played, None if there are 
        more than one pawn or if board and currentBoard are same
        '''

        pawn = None
        if (playerColor == pl.Player.RED):
            myPawn = [bd.Pawns.RED_KING, bd.Pawns.RED]
        else:
            myPawn = [bd.Pawns.BLUE, bd.Pawns.BLUE_KING]

        for x in range (board.SIZE_X):
            for y in range(board.SIZE_Y):
                try:
                    if (captureBoard.getSquare(x,y) == bd.Pawns.NULL):
                        if (board.getSquare(x,y) in myPawn):
                            if (pawn != None):
                                return None
                            pawn = (x,y)
                except bd.SquareNotValid :
                    pass

        return pawn
    def _drawMovement(self, image, mvt):
        for i in range (len(mvt)-1):
            self._camera.drawLineBetweenToPawns(image,mvt[i][0],mvt[i][1],mvt[i+1][0],mvt[i+1][1])

    def getPawnWanted(self, board, availableMovements, playerColor):
        '''
        Request the pawn wanted to play
        '''
        
        self._movement = []
        while (len(self._movement) == 0):
            image = self._camera.captureScreen()
            captureBoard = self._camera.getBoard(image)

            for x in range (board.SIZE_X):
                for y in range(board.SIZE_Y):
                    try:
                        pawn = board.getSquare(x,y)
                        if (pawn == bd.Pawns.RED or pawn == bd.Pawns.RED_KING):
                            self._camera.showPawn(image, (x,y), color=(0,0,255))
                        elif (pawn == bd.Pawns.BLUE or pawn == bd.Pawns.BLUE_KING):
                            self._camera.showPawn(image, (x,y), color=(255,0,0))
                    except bd.SquareNotValid :
                        pass

            for mvt in availableMovements:
                pawn = mvt[0]
                self._camera.showPawn(image, pawn)

            pawn = self._getPawnPlayed(captureBoard, board, playerColor)
            if (pawn != None):
                myMovements = []
                for mvt in availableMovements:
                    if (mvt[0] == pawn):
                        myMovements.append(mvt)

                # Show the mouvement of the selected pawn
                for mvt in myMovements:
                    self._drawMovement(image, mvt)

                nbMovement = 0
                for mvt in myMovements:
                    estimatedBoard = self._getBoardWithMovement(board, mvt)
                    compareCaptureBoard = self._compareBoard(estimatedBoard, captureBoard)
                    if (compareCaptureBoard == True):
                        nbMovement +=1
                        self._movement = mvt
                if (nbMovement != 1):
                    self._movement = []
        
            self._camera.showImage(image, wait=True)
        
        pawnType = board.getSquare(pawn[0], pawn[1])
        if ((pawnType == bd.Pawns.BLUE or pawnType == bd.Pawns.RED) and self._movement[len(self._movement)-1][1] == 0):
            msg = "Wait for putting a King |----------|"
            print(msg,end='')
            for i in range(10):
                time.sleep(1)
                msg = msg.replace('-', 'x', 1)
                print("\r", end='')
                print(msg, end='')
            print("")
        
        image = self._camera.captureScreen()
        self._drawMovement(image, self._movement)
        self._camera.showImage(image, wait=True)

        print("Pawn played: " + str(pawn))

        return pawn

    def getMovementWanted(self):
        '''
        Request the mouvement wanted
        '''

        print("Move done: " + str(self._movement[1:]))

        return self._movement[1:]