import numpy as np

class SquareNotValid(Exception):
    pass
class PawnsException(Exception):
    pass

class Pawns:
    NULL = 0
    RED_KING = 1
    RED = 2
    BLUE_KING = 3
    BLUE = 4

    @staticmethod
    def display(id):
        switcher={
            Pawns.NULL:'   ',
            Pawns.RED_KING:' R ',
            Pawns.RED:' r ',
            Pawns.BLUE_KING:' B ',
            Pawns.BLUE:' b '
        }
        return switcher.get(id,' ')

class Board: 
    SIZE_X=10
    SIZE_Y=SIZE_X
    def __init__(self): 
        self.reset()

    def copy(self):
        """
        Copy constructor
        """
        newBoard = Board()
        newBoard._board = np.copy(self._board)
        return newBoard
    
    def reset(self):
        """
        Reset the _board
        """
        self.resetEmpty()
        for i in range (self.SIZE_Y):
            for j in range (self.SIZE_X//2):
                if (i<(self.SIZE_Y -2)//2):
                    self._board[i][j] = Pawns.BLUE
                elif (i>=(self.SIZE_Y -2)/2 + 2):
                    self._board[i][j] = Pawns.RED
    
    def resetEmpty(self):
        """
        Reset the _board with no pawns
        """
        self._board=np.zeros((self.SIZE_Y,self.SIZE_X//2), dtype=int)


    def display(self):
        """
        Display the matrix _board in the correct form of play
        """
        line = '   '
        for i in range(self.SIZE_X):
            line = line + str(i) + '   '
        print(line)

        for i in range (self.SIZE_Y):
            line = str(i) + '|'
            for j in range (self.SIZE_X):
                if j%2 == i%2:
                    line = line + Pawns.display(self._board[i][j//2]) + '|'
                else:
                    line = line + '   |'
            print (line)

    def getSquare(self,x,y):
        """
        Return the value of the square x,y in the global board
        """
        i,j = self._convertXYtoIJ(x,y)
        return self._board[i][j]
    
    def setSquare(self,x,y,idPawn):
        '''
        Put the pawn idPawn in the square (x,y)
        '''
        i,j=self._convertXYtoIJ(x,y)
        self._board[i][j] = idPawn

    def _convertXYtoIJ(self,x,y):
        """
        Private method

        Convert the x,y coordinates from the global board to i,j coordinates from the matrix _board
        Throws an exception if the square is not playable
        """
        if ((x+y)%2 == 0 and x>=0 and y>=0 and y<self.SIZE_Y and x<self.SIZE_X): # we have pawns only in these squares
            j = x//2 #lines
            i = y #rows
        else:
            raise SquareNotValid("The case (" + str(x) +","+ str(y) + ") is not valid")
            #raise Exception("toto")
        return(i,j)

if __name__ == "__main__": #tests
    b=Board()
    b.display()
    print(b._board)
    print(b._convertXYtoIJ(6,0))
    print(b._board[6][0])
    try:
        print(b.getSquare(10,0))
    except SquareNotValid as identifier:
        print (identifier)
    b.setSquare(0,2,3)
    b.display()