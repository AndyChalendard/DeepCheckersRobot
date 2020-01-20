import serial as ser
import time
import board as bd
import numpy as np
import sys
import glob

class RobotMessageId:
    INIT = 0
    NOINFO = 1
    PONG = 2
    POSITION = 3
    OK = 4


class RobotCom:
    def __init__(self):
        '''
        Constructor, open the serial port and wait the initialization of the robot before doing something
        '''
        self._prevX = None
        self._prevY = None
        self._prevZ = None

        numPort= None
        while (numPort == None):
            print("___________________________________")
            print("Choose the serial port :")
            listePorts = self._listSerialPorts()
            for i in range (len(listePorts)):
                print(i, ") ",listePorts[i])
            print("Press enter to refresh ... ")
            print("___________________________________")
            try:
                numPort = int(input(""))
                self._serial = ser.Serial(listePorts[numPort],9600)# open serial port
                if(self.ping() == False):
                    print("")
                    print("****")
                    print("ERROR: The robot doesn't respond: check the connection...")
                    print("****")
                    numPort = None
                else:
                    while(self._read() != RobotMessageId.INIT): #we expect the initialization of the robot
                        time.sleep(0.1)
            except ValueError:
                numPort= None
                pass
            except IndexError:
                numPort= None
                pass
            except ser.serialutil.SerialException:
                numPort= None
                print("")
                print("****")
                print("ERROR: The robot doesn't respond: check the serial port...")
                print("****")
                pass



    def _listSerialPorts(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'): #WINDOWS
            ports = ['COM%s' % (i + 1) for i in range(256)]
            result = []
            for port in ports:
                try:
                    s = ser.Serial(port)
                    s.close()
                    result.append(port)
                except (OSError, ser.SerialException):
                    pass
            return result
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'): #LINUX
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'): #MAC OS
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')            
        return ports

    def _read(self):
        '''
        Read the lines of the log of the robot
        Return the state where we are
        '''
        while (self._serial.in_waiting > 0): #there are bytes to read
            line = self._serial.readline() 
            line = str(line).split("'")[1].split("\\")[0]
            print("ROBOT: " + line)
            if ("#READY;" in line):
                return RobotMessageId.INIT
            elif ("#PONG;" in line):
                return RobotMessageId.PONG
            elif ("#POS_OK;" in line):
                return RobotMessageId.POSITION
            elif ("#OK;" in line):
                return RobotMessageId.OK
        return RobotMessageId.NOINFO

    def _write(self,text):
        '''
        To send things to the robot
        '''
        for char in text:
            self._serial.write(char.encode('ascii'))
            time.sleep(0.1)

    def ping(self):
        '''
        Check the sending to the robot #PING
        return True if the robot respond
        '''
        self._write("#PING:;")
        if(self._read() == RobotMessageId.PONG):
            return True
        return False
    
    def setMagnet(self,activate):
        '''
        Activate the magnet if activate = True and deactivate else
        return True if the robot respond
        '''
        if (activate):
            self._write("#MAGNET:1;")
        else :
            self._write("#MAGNET:0;")
        if (self._read() != RobotMessageId.OK):
            return False
        return True

    def _putPosition(self,x,y,z):
        self._write("#")
        if(self._prevX != x):
            self._prevX = x
            self._write("POS_X:" + str(x) +";")
        if (self._prevY != y):
            self._prevY = y
            self._write("POS_Y:" + str(y) +";")
        if(self._prevZ != z):
            self._prevZ = z
            self._write("POS_Z:" + str(z) +";")

    def setPosition(self,x,y,z,xSuiv=None,ySuiv=None,zSuiv=None):
        '''
        Send a position in function of x, y , z
        return True if the robot respond
        '''
        self._putPosition(x,y,z)
        self._write("POS_GO:;")
        if (self._read() != RobotMessageId.OK):
            return False
        if (xSuiv and ySuiv and zSuiv):
            self._putPosition(xSuiv,ySuiv,zSuiv)
        while(self._read() != RobotMessageId.POSITION):
            time.sleep(0.01)

        return True

    def close(self):
        '''
        Close the serial port
        '''
        self._serial.close()
    
class RobotCheckers :

    #Caracteristics of the real board
    SIZE_X_REAL = 245 
    SIZE_Y_REAL = 245

    #Center to center
    X_MIN = - SIZE_X_REAL//2
    X_MAX = SIZE_X_REAL//2
    Y_MIN = 130  #Distance between the robot and the board
    Y_MAX = 130 + SIZE_Y_REAL

    X_PAWN_STACK= X_MIN-55 #Coordonates of the pawns stack to take
    Y_PAWN_STACK = (Y_MAX+Y_MIN)//2

    X_PAWN_DROP = -360 #Coordonates of the position to drop pawns
    Y_PAWN_DROP = 50

    PAWNS_STACK = 10 #Number of pawns in the stack in home

    HOME_X = X_MIN-25
    HOME_Y = Y_MIN
    HOME_Z = 30

    def __init__ (self):
        self._robot = RobotCom()
        self.reset()

    def reset (self):
        '''
        Reset the robot
        '''
        self._caughtPawn = False
        self._pawnsHome = self.PAWNS_STACK
        self.goHome()

    def closeRobot(self):
        '''
        Destructor, close the serial port
        '''
        self._robot.setMagnet(activate = False)
        self._robot.close()


    def checkBoard(self):
        '''
        Check the 4 angles of the board to calibrate the X_MIN & Y_MIN & X_MAX & Y_MAX
        '''
        self._robot.setPosition(self.X_MIN,self.Y_MIN,20,self.X_MIN,self.Y_MIN,5)
        self._robot.setPosition(self.X_MIN,self.Y_MIN,5)
        time.sleep(2)
        self._robot.setPosition(self.X_MIN,self.Y_MAX,20,self.X_MIN,self.Y_MAX,5)
        self._robot.setPosition(self.X_MIN,self.Y_MAX,5)
        time.sleep(2)
        self._robot.setPosition(self.X_MAX,self.Y_MAX,20,self.X_MAX,self.Y_MAX,5)
        self._robot.setPosition(self.X_MAX,self.Y_MAX,5)
        time.sleep(2)
        self._robot.setPosition(self.X_MAX,self.Y_MIN,20,self.X_MAX,self.Y_MIN,5)
        self._robot.setPosition(self.X_MAX,self.Y_MIN,5)
        time.sleep(2)
    
    def createBoard(self,board):
        '''
        Create the real board
        '''
        for i in range(board.SIZE_X):
            for j in range(board.SIZE_Y):
                try:
                    pawn = board.getSquare(i,j)
                    if (pawn != bd.Pawns.NULL):
                        self._robot.setPosition(0,300,100)
                        self._robot.setMagnet(activate=True)
                        self._caughtPawn=True
                        print("Je veux un pion : " + bd.Pawns.display(pawn))
                        input()
                        self.putPawn((i,j),board)
                except bd.SquareNotValid:
                    pass
        self.goHome()
                
    def _convertSquareToMovement(self,square,board):
        '''
        Convert the square from the board terminal to the real board for the robot
        Return x,y which is the coordonates of the real board
        '''
        spaceSquareX = (self.X_MAX - self.X_MIN)//(board.SIZE_X-1)
        spaceSquareY = (self.Y_MAX - self.Y_MIN)//(board.SIZE_Y-1)
        x = square[0]*spaceSquareX + self.X_MIN
        y = ((board.SIZE_Y-1)-square[1])*spaceSquareY + self.Y_MIN
        return x,y

    def catchPawn(self, square, board):
        '''
        Catch a pawn in the real board if the robot have no pawn in this time
        Return True if the robot has succeded to take the pawn
        '''
        if (self._caughtPawn == False):
            x,y=self._convertSquareToMovement(square,board)
            self._robot.setPosition(x,y,20,x,y,5)
            self._robot.setPosition(x,y,5,x,y,20)
            self._caughtPawn = self._robot.setMagnet(activate=True)
            self._robot.setPosition(x,y,20)
            return self._caughtPawn
        return False

    def putPawn(self,square,board):
        '''
        Put a pawn in the specified square
        Return True if the robot has succeded to put the pawn
        '''
        if (self._caughtPawn == True):
            x,y=self._convertSquareToMovement(square,board)
            self._robot.setPosition(x,y,20,x,y,5)
            self._robot.setPosition(x,y,5,x,y,20)
            self._robot.setMagnet(activate=False)
            self._caughtPawn = False
            self._robot.setPosition(x,y,20)
            return True
        return False

    def goHome(self):
        '''
        Go to the home position
        '''
        self._robot.setPosition(self.HOME_X,self.HOME_Y,self.HOME_Z)

    def takePawnFromStack(self):
        '''
        Take a pawn in the home position where the stack is
        '''
        if (self._pawnsHome != 0 and self._caughtPawn == False):
            self._robot.setPosition(self.X_PAWN_STACK,self.Y_PAWN_STACK,100,self.X_PAWN_STACK,self.Y_PAWN_STACK,5*self._pawnsHome)
            self._robot.setPosition(self.X_PAWN_STACK,self.Y_PAWN_STACK,5*self._pawnsHome,self.X_PAWN_STACK,self.Y_PAWN_STACK,100)
            self._caughtPawn = self._robot.setMagnet(activate=True)
            if (self._caughtPawn):
                self._pawnsHome = self._pawnsHome - 1
            self._robot.setPosition(self.X_PAWN_STACK,self.Y_PAWN_STACK,100)
    
    def dropPawn(self):
        '''
        Drop a pawn in the position where there are dropped pawns
        '''
        if (self._caughtPawn == True):
            self._robot.setPosition(self.HOME_X,self.HOME_Y,self.HOME_Z,self.X_PAWN_DROP,self.Y_PAWN_DROP,100)
            self._robot.setPosition(self.X_PAWN_DROP,self.Y_PAWN_DROP,100,self.HOME_X,self.HOME_Y,self.HOME_Z)
            self._robot.setMagnet(activate=False)
            self._caughtPawn = False
            self.goHome()
    
    def jumpPawn(self,squares,board):
        '''
        squares : list of square
        Go in these squares but don't put it in theses squares
        (It is when there are several pawns to jump)
        '''
        for square in squares:
            x,y=self._convertSquareToMovement(square,board)
            self._robot.setPosition(x,y,30,x,y,20)
            self._robot.setPosition(x,y,20)


class GameRobot :
    def __init__(self):
        self._robotCheckers = RobotCheckers()

    def reset(self):
        '''
        Reset the gameRobot
        '''
        self._robotCheckers.reset()

    def _AddKing(self,square,board):
        '''
        Take a pawn from kings stack and put it in the specified square
        We consider that the robot is a RED player
        '''
        self._robotCheckers.catchPawn(square,board)
        self._robotCheckers.dropPawn()
        self._robotCheckers.takePawnFromStack()
        self._robotCheckers.putPawn(square,board)

    def _jumpPawns(self,jumpedPawns,board):
        '''
        JumpedPawns : list of square : (..,..)
        Take a pawn and drop it when there are jumpedPawns
        '''
        for pawns in jumpedPawns:
            self._robotCheckers.catchPawn(pawns,board)
            self._robotCheckers.dropPawn()
    
    
    #Main function
    def movePawn(self,squarePawn,squareMov,jumpedPawns,goToKing,movement,board):
        '''
        Move a pawn from squarePawn to squareMov
        '''
        self._robotCheckers.catchPawn(squarePawn,board)
        
        if (len(movement) > 1): #there are several squares to jump
            self._robotCheckers.jumpPawn(movement,board)

        self._robotCheckers.putPawn(squareMov,board)
        if (goToKing):
            self._AddKing(squareMov,board)

        if (len(jumpedPawns) != 0):
            self._jumpPawns(jumpedPawns,board)

        self._robotCheckers.goHome()





if __name__ == "__main__": #tests

    #TEST DU ROBOTCOM
    '''
    r = RobotCom()
    if (r.ping()):
        print("Robot detecté")
        while(1):
            x=int(input("X ?"))
            y=int(input("Y ?"))
            z=int(input("Z ?"))
            r.setPosition(x,y,z)
        r.close()
    '''

    #TEST DU ROBOTCHECKERS
    board = bd.Board()
    rc = RobotCheckers()
    '''
    #Test du convertisseur & checkBoard / catch / put (besoin de calibrer le plateau)

    rc.checkBoard()
    pause = input()
    rc.catchPawn((0,7),board)
    rc.putPawn((2,5),board)
    rc.catchPawn((1,6),board)
    rc.dropPawn()

    #Test du home/ drop/ take (besoin de connaitre les positions du drop et take)

    while(1):
        time.sleep(3)
        rc.takePawnFromStack() 
        rc.dropPawn()
    '''
    rc.createBoard(board)





