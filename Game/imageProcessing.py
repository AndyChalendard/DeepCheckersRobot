import cv2
import numpy as np

class Image:

    _sizeX = None
    _sizeY = None

    _rgb = None
    _hsv = None
    _hsvDef = False

    def __init__(self, rgb):
        self._rgb = rgb
        self._hsv = None
        _hsvDef = False
        self._sizeX = None
        self._sizeY = None

    def getSizeX(self):
        if (self._sizeX == None):
            self._sizeX = len(self._rgb[0])
            
        return self._sizeX

    def getSizeY(self):
        if (self._sizeY == None):
            self._sizeY = len(self._rgb)
            
        return self._sizeY

    def getHsv(self):
        if (self._hsvDef == False):
            self._hsvDef = True
            self._hsv = cv2.cvtColor(self._rgb, cv2.COLOR_BGR2HSV)
        
        return self._hsv

    def getRgb(self):
        return self._rgb


class Camera:

    NAME = "Checkers"

    _areaSelected = []

    def __init__(self):
        self._camera = cv2.VideoCapture(0)

    def _clickImage(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self._areaSelected = [(x, y)]
        elif event == cv2.EVENT_LBUTTONUP:
            self._areaSelected.append((x, y))

    def _captureScreen(self):
        ret, im = self._camera.read()

        image = Image(im)

        key = cv2.waitKey(10)

        return image

    def _searchPawnsMask(self, image):
        hsv = image.getHsv()

        # define range of blue color in HSV
        lower_red = np.array([0,40,20])
        upper_red = np.array([20,255,255])
        maskRed = cv2.inRange(hsv, lower_red, upper_red)
        
        lower_red = np.array([150,40,20])
        upper_red = np.array([255,255,255])
        maskRed = cv2.bitwise_or(cv2.inRange(hsv, lower_red, upper_red), maskRed)

        lower_blue = np.array([60,20,0])
        upper_blue = np.array([140,255,255])
        maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)

        return cv2.bitwise_or(maskBlue, maskRed)

    def _showImage(self, image):
        rgb = image.getRgb()

        if (len(self._areaSelected) == 2):
            # draw a rectangle around the region of interest
            cv2.rectangle(rgb, self._areaSelected[0], self._areaSelected[1], (0, 255, 0), 2)

        cv2.imshow(self.NAME, rgb)
        cv2.namedWindow(self.NAME)
        cv2.setMouseCallback(self.NAME, self._clickImage)

if __name__ == "__main__":

    cam = Camera()
    
    key = -1

    while key != 113:
        im = cam._captureScreen()
        pawnMask = cam._searchPawnsMask(im)

        # Bitwise-AND mask and original image
        im = Image(cv2.bitwise_and(im.getRgb(),im.getRgb(), mask= pawnMask))

        gray = cv2.cvtColor(im.getRgb(), cv2.COLOR_BGR2GRAY)
        #ret,thresh = cv2.threshold(gray,100,200,cv2.THRESH_BINARY_INV)
        ret,thresh = cv2.threshold(gray,0,30,cv2.THRESH_BINARY)
        #thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,5,6)
        contours,h = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            perimetre=cv2.arcLength(cnt,True)
            if (perimetre > 100):
                approx = cv2.approxPolyDP(cnt,0.01*perimetre,True)

                M = cv2.moments(cnt)
                if (M["m00"] != 0):
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    if (cX < im.getSizeX()-3 and cX > 3 and cY < im.getSizeY()-3 and cY > 3):
                        cv2.drawContours(im.getRgb(),[cnt],-1,(0,255,0),2)

                        if len(approx) < 10:
                            shape = "King"
                        else:
                            shape= "simple"
                        cv2.putText(im.getRgb(), shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
                        
                        for i in range (-2,3):
                            for j in range(-2,3):
                                im.getRgb()[cY+i][cX+j][1] = 255
                

        #im = Image(img)

        #cam._showImage(Image(thresh))
        cam._showImage(im)

        #key = cv2.waitKey(1000)