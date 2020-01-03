
class Player:
    RED = 0
    BLUE = 1

    def __init__(self,color,isHuman): 
        self._color = color
        self.isHuman = isHuman

    def getColor(self):
        '''
        Get the color of the player (RED or BLUE)
        '''
        return self._color

    def getPawnWanted(self):
        '''
        Get the pawn that the player wants to play with
        '''
        if self.isHuman :
            coord = input("Enter the pawn you want move : x y\n").split()
            if (len(coord) > 2):
                raise Exception("Enter only x y") 
            xPawn = int(coord[0])
            yPawn = int (coord[1])
        return xPawn, yPawn

    def getMovementWanted(self):
        """
        Get the movement that the player wants to do
        """
        if self.isHuman :
            coord = input("Enter the coordonates of the movement : x y\n ").split()
            if (len(coord) > 2):
                raise Exception("Enter only x y") 
            xMov = int(coord[0])
            yMov = int (coord[1])
        return xMov, yMov
        



if __name__ == "__main__": #tests
    p1 = Player(Player.RED,True)
    p2 = Player(Player.BLUE,True)
    print(p1.getColor())
    print(p2.getColor())
    #t,s= raw_input().split()
    #print(t)

    x,y=p1.getPawnWanted()
    z,w=p1.getMovementWanted()
    print(x,y)
    print(z,w)