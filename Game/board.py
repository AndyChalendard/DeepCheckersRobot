import numpy as np

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
    SIZE_X=12
    SIZE_Y=8
    def __init__(self): 
        self._board=np.zeros((self.SIZE_X,self.SIZE_Y/2))
        self.reset()
    
    def reset(self):
        for i in range (self.SIZE_X):
            for j in range (self.SIZE_Y/2):
                if (i<(self.SIZE_X -2)/2):
                    self._board[i][j] = Pawns.BLUE
                elif (i>=(self.SIZE_X -2)/2 + 2):
                    self._board[i][j] = Pawns.RED

    def display(self):
        for i in range (self.SIZE_X):
            line = '|'
            for j in range (self.SIZE_Y/2):
                if j%2 == i%2:
                    line = line + Pawns.display(self._board[i][j]) + '|'
                else:
                    line = line +'   '+ '|' + Pawns.display(self._board[i][j]) + '|' +'   '+ '|'
            print (line)

if __name__ == "__main__": #tests    
    b=Board()
    b.display()






