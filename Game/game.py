import board
import player

class Game:
    def __init__(self):
        self._board = board.Board()
    
    def getBoard(self):
        return self._board

    def getAvailableMovement(self,square,player):
        x = square[0]
        y = square[1]
        color = self._board.getSquare(x,y)

        available = []
        if (color == 0) : #square empty
            raise Exception("No pawn in this square") 
        else :
            if (player.getColor() == 0):
                if (color != 1 and color !=2): #not using his pawn
                    raise Exception("It is not your pawn !")
            else :
                if (color != 3 and color !=4): #not using his pawn
                    raise Exception("It is not your pawn !")
            
            if (color == 2 or color == 4): #for simple pawn
                if (color == 4): #at the top of the board
                    if (y != 0 and x != self._board.SIZE_X-1 and self._board.getSquare(x+1,y+1) == 0):
                        available.append((x+1,y+1))
                    if (x!=0 and y != 0 and self._board.getSquare(x-1,y+1) == 0):
                        available.append((x-1,y+1))

                if (color == 2): #at the bottom
                    if (x != self._board.SIZE_X-1 and y!= self._board.SIZE_Y -1 and self._board.getSquare(x+1,y-1) == 0):
                        available.append((x+1,y-1))
                    if (x!=0 and y!= self._board.SIZE_Y -1 and self._board.getSquare(x-1,y-1) == 0):
                        available.append((x-1,y-1))
            #else: #for kings TODO

        return available

if __name__ == "__main__":
    g=Game()
    b = g.getBoard()
    b.display()
    #print(b.getSquare(2,2))

    p = player.Player(0,True) #red
    #g.getAvailableMovement((0,2),p) #not your pawn
    #g.getAvailableMovement((0,5),p) #square not valid
    print(g.getAvailableMovement((0,6),p)) #nothing there is always a pawn in (1,5)
    print(g.getAvailableMovement((1,5),p)) #works
    print(g.getAvailableMovement((7,5),p)) #works

    p = player.Player(1,True) #blue
    print(g.getAvailableMovement((0,0),p)) #nothing there is always a pawn in (1,5)
    print(g.getAvailableMovement((2,2),p)) #works
    print(g.getAvailableMovement((0,2),p)) #works

