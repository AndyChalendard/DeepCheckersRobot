import random
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

    def getPawnWanted(self,validPawns):
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
            print("Player choose the pawn: " + str((xPawn,yPawn)))
        return xPawn, yPawn

    def getMovementWanted(self,validMovements):
        """
        Get the movement that the player wants to do
        """

        finalMovement = []
        for elt in validMovements:
            finalMovement.append(elt[len(elt)-1])
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
            print("and move to " + str((xMov,yMov)))
        return xMov, yMov
        



if __name__ == "__main__": #tests
    p1 = Player(Player.RED,True)
    p2 = Player(Player.BLUE,True)
    print(p1.getColor())
    print(p2.getColor())