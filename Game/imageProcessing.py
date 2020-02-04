import cv2
import numpy as np
import board as bd

class Image:
    # Contain an image

    # Size of the image
    _sizeX = None
    _sizeY = None

    # Array in different type of the image
    _rgb = None
    _hsv = None

    # If the hsv image is figure out
    _hsvDef = False

    def __init__(self, rgb):
        self._rgb = rgb
        self._hsv = None
        _hsvDef = False
        self._sizeX = None
        self._sizeY = None

    def getSizeX(self):
        #return the X size of the image
        if (self._sizeX == None):
            self._sizeX = len(self._rgb[0])
            
        return self._sizeX

    def getSizeY(self):
        # return the Y size of the image
        if (self._sizeY == None):
            self._sizeY = len(self._rgb)
            
        return self._sizeY

    def getHsv(self):
        # return the hsv image
        if (self._hsvDef == False):
            self._hsvDef = True
            self._hsv = cv2.cvtColor(self._rgb, cv2.COLOR_BGR2HSV)
        
        return self._hsv

    def getRgb(self):
        # return the rgb image
        return self._rgb

class AreaRect:
    # Working area class

    # Coordinate of the window
    xMin = None
    xMax = None
    yMin = None
    yMax = None

    def __init__(self, x1, y1, x2, y2):
        if (x1 > x2):
            self.xMin = x2
            self.xMax = x1
        else:
            self.xMin = x1
            self.xMax = x2
        if (y1 > y2):
            self.yMin = y2
            self.yMax = y1
        else:
            self.yMin = y1
            self.yMax = y2
    
    def getPt1(self):
        # Return the point in the top corner left
        return (self.xMin, self.yMin)
    
    def getPt2(self):
        # Return the point in the bottom corner right
        return (self.xMax, self.yMax)
    
    def getArea(self):
        # get the sarea of the volume
        return (self.xMax-self.xMin)*(self.yMax-self.yMin)
    
    def pointIsInArea(self, x, y):
        # return true if the point given is in the working area
        if (self.xMin<x and x<self.xMax):
            if (self.yMin<y and y<self.yMax):
                return True
        return False

class Camera:
    # Class who manage the camera

    # Name of the window opened to show the image
    NAME = "Checkers"

    # If the new working area is needed (click event is made)
    _requireArea = True
    # Working area variable
    _areaSelected = None

    # Board array of the pixel position and the contour of the pawn
    _checkersSquarePosition = None

    def __init__(self):
        self._camera = cv2.VideoCapture(0)

        # Waiting for the selection of working area
        key = -1
        while (key != 113 or self._areaSelected == None or self._areaSelected.getArea() <= 80000):
            key = -1

            image = self.captureScreen()

            if (self._areaSelected == None):
                cv2.putText(image.getRgb(), "No area selected !", (10, image.getSizeY()-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
            elif (self._areaSelected.getArea() <= 80000):
                cv2.putText(image.getRgb(), "Area too small !", (10, image.getSizeY()-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
            else:
                cv2.putText(image.getRgb(), "Tap 'q' when the selected area is good", (10, image.getSizeY()-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
            
            self.showImage(image)
            key = cv2.waitKey(10)

        self._requireArea = False
        print("Working area selected")

        # Detection of the position of the board
        boardValid = False
        while (boardValid == False):
            # Detect square position
            checkersSquarePosition = []
            key = -1
            while (len(checkersSquarePosition) != 32 or key != 111):
                key = -1

                imShow = self.captureScreen()

                # Apply blur to split square
                blur_image = Image(cv2.blur(imShow.getRgb(),(23,23)))

                squareMaskYellow = self._getMaskYellowSquare(blur_image)
                
                imFiltered = Image(cv2.bitwise_and(blur_image.getRgb(),blur_image.getRgb(), mask=squareMaskYellow))
                checkersSquarePosition = self._findContour(imFiltered, imFiltered, True, "case")

                if (len(checkersSquarePosition) != 32):
                    cv2.putText(imFiltered.getRgb(), "Board square is not detect", (10, imShow.getSizeY()-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                else:
                    cv2.putText(imFiltered.getRgb(), "Board OK, you can press 'o' to valid detection", (10, imShow.getSizeY()-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)

                self.showImage(imFiltered)
                key = cv2.waitKey(10)

            self._checkersSquarePosition = [[None for i in range(0, bd.Board().SIZE_X)] for i in range(0,bd.Board().SIZE_Y)]

            for j in range(0, bd.Board().SIZE_Y):
                # We search the Y higher remaining point
                currentPoint = []
                for i in range(0, bd.Board().SIZE_X//2):
                    posY = self._getPointPositionMax(checkersSquarePosition, 1)
                    point = checkersSquarePosition[posY]
                    currentPoint.append(point)
                    checkersSquarePosition.remove(point)

                # We search the most left point and put in the boardtab
                for i in range(0, len(currentPoint)):
                    pos = self._getPointPositionMax(currentPoint, 0)
                    point = currentPoint[pos]
                    self._checkersSquarePosition[j][i*2+(j%2)] = point
                    currentPoint[pos] = (0, 0, None)
            
            # We show the coord in the screen
            imShow = self.captureScreen()
            self.showBoardPoint(imShow)
            self.showImage(imShow)
            key = cv2.waitKey(1000)

            tap = input("Do you want valid the board ? (y/N)")
            if (tap == "y" or tap == "Y"):
                boardValid = True
    
    def _getPointPositionMax(self, points, coord = 0):
        # Get the minimum position in the tab, on the coord (1:x ; 0:y)
        m = points[0][coord]
        position = 0
        for i in range(0, len(points)):
            if (points[i][coord] > m):
                m = points[i][coord]
                position = i
        return position

    def showBoardPoint(self, imShow):
        # Show the board with the coord detect
        for y in range(0, bd.Board().SIZE_Y):
            for x in range(0, bd.Board().SIZE_X):
                case = self._checkersSquarePosition[y][x]
                if (case != None):
                    self._drawCrossAndText(imShow, "("+str(x)+":"+str(y)+")", case[0], case[1])

    def _drawCrossAndText(self, im, text, x, y, color = (0,0,0), crossSize = 3):
        # Show a cross and a text in the position (x,y)

        # Show the text if exists
        if (text):
            cv2.putText(im.getRgb(), text, (x-(4*len(text)), y-10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 2)
        
        # Show the cross
        for i in range (-crossSize,crossSize+1):
            im.getRgb()[y+i][x][0] = color[0]
            im.getRgb()[y+i][x][1] = color[1]
            im.getRgb()[y+i][x][2] = color[2]
        for j in range(-crossSize,crossSize+1):
            im.getRgb()[y][x+j][0] = color[0]
            im.getRgb()[y][x+j][1] = color[1]
            im.getRgb()[y][x+j][2] = color[2]

    def _getDistanceBetweenPoint(self, pt1, pt2):
        # return the distance between two pixel
        dist = ((pt1[0]-pt2[0])**2) + ((pt1[1]-pt2[1])**2)

        return dist

    def _getBoardPositionOfPawn(self, pawnPosition):
        # Return the nearest square for the pawn
        x = 0
        y = 0

        if (pawnPosition != None):
            distance = self._getDistanceBetweenPoint(self._checkersSquarePosition[y][x], pawnPosition)
            for j in range(0,len(self._checkersSquarePosition)):
                for i in range(0,len(self._checkersSquarePosition[j])):
                    square = self._checkersSquarePosition[j][i]
                    if (square != None):
                        dist = self._getDistanceBetweenPoint(square, pawnPosition)
                        if (dist < distance):
                            distance = dist
                            x = i
                            y = j

        return (x, y)

    def getBoard(self, im):
        tmpBoard = bd.Board(fullBoard=False)

        # We search the pawn
        for color in range(0,2):
            BLUE = 0
            #RED = 1

            # We figure out the mask of the pawn color
            if (color == BLUE):
                pawnMask = cam._getMaskBluePawns(im)
                pawnColor = bd.Pawns.BLUE
                colorText = "Blue"
            else:
                pawnColor = bd.Pawns.RED
                pawnMask = cam._getMaskRedPawns(im)
                colorText = "Red"
        
            # We figure out the filtered image
            imFiltered = Image(cv2.bitwise_and(im.getRgb(), im.getRgb(), mask=pawnMask))

            # We find the pawn
            pawns = self._findContour(im, imFiltered, showContours=False, text=colorText)

            # We search the pawn position in the board
            for pawn in pawns:
                (x, y) = self._getBoardPositionOfPawn(pawn)
                tmpBoard.setSquare(x , y, pawnColor)

        return tmpBoard

    def showPawn(self, im, squarePosition, color = (0,255,0)):
        # Show the contour of the pawn at the position pawnPosition

        case = self._checkersSquarePosition[squarePosition[1]][squarePosition[0]]

        self._drawCrossAndText(im, None, case[0], case[1], color=color, crossSize=10)

    def _clickImage(self, event, x, y, flags, param):
        # Click event on the image
        if (self._requireArea == True):
            if event == cv2.EVENT_LBUTTONDOWN:
                self._tmpXClick = x
                self._tmpYClick = y
            elif event == cv2.EVENT_LBUTTONUP:
                self._areaSelected = AreaRect(x,y, self._tmpXClick, self._tmpYClick)

    def captureScreen(self):
        # Get the image capture by camera
        _, im = self._camera.read()

        image = Image(im)

        return image

    def _getMaskRedPawns(self, image):
        # Get the mask for the red color
        hsv = image.getHsv()

        # define range of blue color in HSV
        lower_red = np.array([0,40,20])
        upper_red = np.array([20,255,255])
        maskRed = cv2.inRange(hsv, lower_red, upper_red)
        
        lower_red = np.array([150,40,20])
        upper_red = np.array([255,255,255])
        maskRed = cv2.bitwise_or(cv2.inRange(hsv, lower_red, upper_red), maskRed)

        return maskRed

    def _getMaskBluePawns(self,image):
        # Get the mask of the blue color
        hsv = image.getHsv()

        lower_blue = np.array([60,60,0]) #60 20 0
        upper_blue = np.array([140,255,255])
        maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)

        return maskBlue

    def _getMaskYellowSquare(self,image):
        # Get the mask of the yellow color
        hsv = image.getHsv()

        lower_yellow = np.array([20,150,0])
        upper_yellow = np.array([50,255,255])
        maskYellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        return maskYellow

    def showImage(self, image):
        # Show the image and the working area
        rgb = image.getRgb()

        if (self._areaSelected != None):
            # draw a rectangle around the region of interest
            cv2.rectangle(rgb, self._areaSelected.getPt1(), self._areaSelected.getPt2(), (0, 255, 0), 2)

        cv2.imshow(self.NAME, rgb)
        cv2.namedWindow(self.NAME)
        cv2.setMouseCallback(self.NAME, self._clickImage)

    def _findContour(self, imageShow,imageFiltered, showContours=True, text=None):
        # Search the contours of the image, return tab wich contain the coord in x and y, and the contour of the object
        centerPoint = []

        # We search the contour
        gray = cv2.cvtColor(imageFiltered.getRgb(), cv2.COLOR_BGR2GRAY)
        _,thresh = cv2.threshold(gray,0,30,cv2.THRESH_BINARY)
        contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            perimetre=cv2.arcLength(cnt,True)
            # If the detected object is large enought
            if (perimetre > 120):

                M = cv2.moments(cnt)
                if (M["m00"] != 0):

                    # We figure out the center of the element
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    if (self._areaSelected.pointIsInArea(cX, cY) == True):
                        if (showContours):
                            cv2.drawContours(imageShow.getRgb(),[cnt],-1,(0,255,0),2)

                        self._drawCrossAndText(imageShow, text, cX, cY)
                        
                        centerPoint.append((cX, cY))
        return centerPoint

if __name__ == "__main__":

    cam = Camera()
    
    while True:
        im = cam.captureScreen()
        board = cam.getBoard(im)

        cam.showBoardPoint(im)

        board.display()

        for x in range(0,board.SIZE_X):
            for y in range(0,board.SIZE_Y):
                try:
                    pawn = board.getSquare(x, y)
                    if (pawn == bd.Pawns.RED):
                        cam.showPawn(im, (x,y), color=(0,0,255))
                    elif (pawn == bd.Pawns.BLUE):
                        cam.showPawn(im, (x,y), color=(255,0,0))
                except bd.SquareNotValid:
                    pass

        cam.showImage(im)
        key = cv2.waitKey(500)


    key = -1

    '''while key != 113:
        imShow = cam.captureScreen()
        key = cv2.waitKey(10)
        pawnMaskBlue = cam._getMaskBluePawns(imShow)
        pawnMaskRed = cam._getMaskRedPawns(imShow)

        # Bitwise-AND mask and original image
        imFilteredBlue = Image(cv2.bitwise_and(imShow.getRgb(),imShow.getRgb(), mask= pawnMaskBlue))
        cam._findContour(imShow, imFilteredBlue, "Blue")
        imFilteredRed = Image(cv2.bitwise_and(imShow.getRgb(),imShow.getRgb(), mask= pawnMaskRed))
        cam._findContour(imShow, imFilteredRed, "Red")

        cam.showImage(imShow)
        key = cv2.waitKey(10)'''