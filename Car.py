import logging, math
from PIL import Image, ImageDraw


class CarModel():
    # class variables common for all instances
    # relative position of car parts
    bodybox = ((-80,45),(-80,65),(-120,0),(-80,-65),(-80,-45),
                (80,-45),(80,-65),(120,0),(80,65),(80,45),(-80,45))

    sensors = ( ((95,-15),(100,-15),(100,-10),(95,-10),(95,-15)),# S0
            ((95,-2.5),(100,-2.5),(100,2.5),(95,2.5),(95,-2.5)), # S1
         ((95,10),(100,10),(100,15),(95,15),(95,10)), # S2
   
    )
    
    wheels = ( ((-8,50),(-8,75),(-72,75),(-72,50),(-8,50)), # rear-right
               ((-8,-50),(-8,-75),(-72,-75),(-72,-50),(-8,-50)), # rear-left
               ((8,-50),(8,-75),(72,-75),(72,-50),(8,-50)), # front-left
               ((8,50),(8,75),(72,75),(72,50),(8,50)) # front-right
    )

    def __init__(self, logLevel=logging.INFO) -> None:
        self.__configLogger(logLevel)
        self._position = (0.0,0.0)
        self._rotation = 0.0 # pointing from top to bottom (south)
        self._scale = 1.0
        return

    def setScale(self, scale) -> None:
        """ By default the simulator use 1 mm = 1 pixel.
        setScale defines the pixel per mm of the orignal car.
        A scale of 2.0 means two pixels per mm (car is drawn bigger), a scale of 0.5 means 0.5 pixels per mm (car is drawn smaller)
        """
        self._scale = scale
        return

    def rotatePoint (self, p):
        angle = math.radians(self._rotation)
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        return (p[0] * cos_theta - p[1] * sin_theta, p[0] * sin_theta + p[1] * cos_theta)

    def translatePoint(self, p):
        return (p[0] + self._position[0], p[1] + self._position[1])

    def scalePoint(self, p):
        return (p[0] * self._scale, p[1] * self._scale)

    def rotateAndTranslatePoints(self, tuples):
        return tuple(self.translatePoint(self.rotatePoint(x)) for x in tuples)
       
    def rotateAndTranslateAndScalePoints(self, tuples):
        return tuple(self.scalePoint(self.translatePoint(self.rotatePoint(x))) for x in tuples)   

    def moveForward(self,x) -> None:
        delta = self.rotatePoint((x,0.0))
        self._position = (self._position[0]+delta[0], self._position[1]+delta[1])
        self._logger.debug(f'moveForward {x}: new position is {self._position}, orientation is {self._rotation}')
        return
    
    def rotate(self, x) -> None:
        self._rotation = self._rotation + x
        self._logger.debug(f'rotate {x}: new position is {self._position}, orientation is {self._rotation}')
        return

    def draw(self, imageDraw) -> None:
        imageDraw.polygon(self.rotateAndTranslateAndScalePoints(self.bodybox), fill=None, outline=(0,0,0), width=2)
        for w in self.wheels:
            imageDraw.polygon(self.rotateAndTranslateAndScalePoints(w), fill=(0,0,0), outline=(0,0,0), width=1)
        for s in self.sensors:
            imageDraw.polygon(self.rotateAndTranslateAndScalePoints(s), fill=(255,0,0), outline=(255,0,0), width=1)
        return

    def __configLogger(self, logLevel):
        """ by default log all INFO level and above messages to stderr with timestamp, module and threadname, level and message
        """
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logLevel)
        self._logger.handlers.clear()
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logLevel)
        console_formatter = logging.Formatter('%(asctime)s - (%(name)s %(threadName)-9s) - %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)
        return

    
    



    