import serial as ser
import time

class RobotMessageId:
    INIT = 0
    NOINFO = 1
    PONG = 2
    POSITION = 3
    OK = 4

class RobotCom:
    def __init__(self):
        '''
        Constructor, open the serial port and expect the initialization of the robot before doing something
        '''
        self._serial = ser.Serial('/dev/tty.usbmodem14203',9600)  # open serial port
        while(self._read() != RobotMessageId.INIT): #we expect the initialization of the robot
            time.sleep(0.1)

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

    def setPosition(self,x,y,z):
        '''
        Send a position in function of x, y , z
        return True if the robot respond
        '''
        self._write("#POS_X:" + str(x) +";")
        if (self._read() != RobotMessageId.OK):
            return False
        self._write("#POS_Y:" + str(y) +";")
        if (self._read() != RobotMessageId.OK):
            return False
        self._write("#POS_Z:" + str(z) +";")
        if (self._read() != RobotMessageId.OK):
            return False
        self._write("#POS_GO:;")
        while(self._read() != RobotMessageId.POSITION):
            time.sleep(0.1)
        return True

    def close(self):
        '''
        Close the serial port
        '''
        self._serial.close()

if __name__ == "__main__": #tests
    r = RobotCom()
    if (r.ping()):
        print("Robot detecté")
        r.setMagnet(True)
        r.setPosition(200,300,100)
        r.setPosition(-200,300,100)
        r.setPosition(300,400,200)
        r.setPosition(0,500,200)
        r.setMagnet(False)
        r.close()







