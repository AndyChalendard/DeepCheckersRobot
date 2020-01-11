import random
import models as mod
class PlayerType:
    HUMAN_TERMINAL = 0
    IA = 1
    RANDOM = 2

class Player:
    RED = 0
    BLUE = 1

    def __init__(self,color,playerType):
        self._color = color
        self._type = playerType
        if (self._type == PlayerType.IA):
            self._IA = mod.IA(8,8) #sizeX sizeY

    def needDisplay(self):
        if(self._type == PlayerType.HUMAN_TERMINAL):
            return True
        else:
            return False

    def getColor(self):
        '''
        Get the color of the player (RED or BLUE)
        '''
        return self._color

    def getPawnWanted(self,validPawns, board):
        '''
        Get the pawn that the player wants to play with
        '''
        xPawn = -1
        yPawn = -1
        if (self._type == PlayerType.HUMAN_TERMINAL) :
            if (self._color == self.RED):
                print("--------RED TURN--------")
            else:
                print("--------BLUE TURN--------")
            while ((xPawn,yPawn) not in validPawns): #this is not a valid pawn
                print("Valid pawn" + str(validPawns))
                coord = input("Enter the pawn you want move : x y\n").split()
                if (len(coord) ==2):
                    xPawn = int(coord[0])
                    yPawn = int (coord[1])
        elif(self._type == PlayerType.RANDOM):
            pawn = random.randint(0, len(validPawns)-1)
            xPawn,yPawn = validPawns[pawn]
            #print("Player choose the pawn: " + str((xPawn,yPawn)))
        elif(self._type == PlayerType.IA):
            tmpBoard = board.copy()
            if (self._color == self.BLUE):
                tmpBoard = board.reverseColor()
            xPawn,yPawn = self._IA.getPawnWanted(tmpBoard, validPawns)
        return xPawn, yPawn

    def getMovementWanted(self,finalMovement, board):
        """
        Get the movement that the player wants to do
        """
        xMov = -1
        yMov = -1
        if (self._type == PlayerType.HUMAN_TERMINAL) :
            while ((xMov,yMov) not in finalMovement): #This is not a valid movement
                print("Valid destination" + str(finalMovement))
                coord = input("Enter the coordonates of the movement : x y\n ").split()
                if (len(coord) == 2):
                    xMov = int(coord[0])
                    yMov = int (coord[1])
        elif(self._type == PlayerType.RANDOM):
            mov = random.randint(0, len(finalMovement)-1)
            xMov,yMov = finalMovement[mov]
            #print("and move to " + str((xMov,yMov)))
        elif(self._type == PlayerType.IA):
            if (self._color == self.BLUE):
                tmpBoard = board.reverseColor()
            else:
                tmpBoard = board.copy()
            xMov,yMov = self._IA.getMovementWanted(tmpBoard, finalMovement)
        return xMov, yMov

    def setReward(self, reward):
        if (self._type == PlayerType.IA):
            self._IA.learn(reward)

    def saveModel(self):
        if (self._type == PlayerType.IA):
            self._IA.saveNeuralNetworks()

    def reset(self):
        if (self._type == PlayerType.IA):
            self._IA.resetIA()

if __name__ == "__main__": #tests
    p1 = Player(Player.RED,True)
    p2 = Player(Player.BLUE,True)
    print(p1.getColor())
    print(p2.getColor())
