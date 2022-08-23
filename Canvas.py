

import logging
import random
import time
from PIL import Image, ImageDraw
import math
from shapely.geometry import LineString
from itertools import chain


class CanvasModel():

    CANVAS_SIZE = (1500, 1200)
    CANVAS_BORDER = 100
    CURVE_WIDTH = 15

    def __init__(self, size=CANVAS_SIZE, border=CANVAS_BORDER, curveWidth=CURVE_WIDTH, seed=time.time(), logLevel=logging.INFO) -> None:
        """
        Create a new canvas with a random curve.
        If you want a reproducible canvas provide a seed (e.g. 5 or 9)
        """
        self.__configLogger(logLevel)
        self._size = size
        self._imgsize = (size[0]+border*2, size[1]+border*2)
        self._border = border
        self._curveWidth = curveWidth
        self._seed = seed
        self.initCurve()
        return

    def initCurve(self):
        """
        initialize a line from left to right that follows bezier curves - 
        the curves depend on the random seed used to initialize the canvas.

        TODO: for the following seed values we have a problem
        for seed value 6 we get a division by zero
        for seed value 7 the car's sensors are not correctly placed on the line
        """
        random.seed(self._seed)
        # two of the 1-6 points are already used for the start and end
        i = random.randint(1, 6)
        x = [self._border]
        x.extend(sorted(random.sample(
            range(self._border, self._size[0]+self._border), i)))
        x.append(self._size[0]+self._border)
        y = random.sample(range(self._border, self._size[1]+self._border), i+2)
        xys = list(zip(x, y))
        ts = [t/20.0 for t in range(21)]

        bezier = make_bezier(xys)
        points = bezier(ts)

        # now extend line into 15 width polygon with shapely
        line = LineString([list(point) for point in points])
        # the buffer() invocation is the essential one extending the line
        newpoints = line.buffer(7.5, cap_style=3, join_style=1)
        self._curvePoints = list(newpoints.exterior.coords)

        # Now compute the car start position.
        # a bezier curve is tangential to the first line given by the points, so we can compute
        # the angle from the line coordinates
        self._delta_y = (xys[1][1]-xys[0][1])/(xys[1][0]-xys[0][0])
        self._angle = math.degrees(math.atan(self._delta_y))
        self._bezierPoints = xys
        self._logger.debug(
            f'Canvas: new Curve: {i} bezier control points, orientation {self._angle}, startpoint {xys[0]}, size {self._size}, border {self._border}')

    def getCurveStartingPoint(self):
        return self._bezierPoints[0]

    def getCurveStartingOrientation(self):
        return self._angle

    def getCurveBoundingPoints(self):
        return self._curvePoints

    def getCanvasBoundingPoints(self):
        return ((self._border, self._border), (self._size[0]+self._border, self._border), (self._size[0]+self._border, self._size[1]+self._border), (self._border, self._size[1]+self._border), (self._border, self._border))

    def createImageAndDraw(self):
        im = Image.new('RGB', self._imgsize, (128, 128, 128))
        imageDraw = ImageDraw.Draw(im)
        imageDraw.rectangle((self._border, self._border, self._size[0]+self._border, self._size[1]+self._border), fill=(
            255, 255, 255), width=1, outline=(255, 255, 255))
        imageDraw.polygon(self._curvePoints, outline='black', fill='black')
        return (im, imageDraw)

    def __configLogger(self, logLevel):
        """ by default log all INFO level and above messages to stderr with timestamp, module and threadname, level and message
            """
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logLevel)
        self._logger.handlers.clear()
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logLevel)
        console_formatter = logging.Formatter(
            '%(asctime)s - (%(name)s %(threadName)-9s) - %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)
        return


# The following functions are copied from
# https://stackoverflow.com/questions/246525/how-can-i-draw-a-bezier-curve-using-pythons-pil
# Copyright https://stackoverflow.com/users/190597/unutbu


def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)

    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier


def pascal_row(n, memo={}):
    # This returns the nth row of Pascal's Triangle
    if n in memo:
        return memo[n]
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n & 1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    memo[n] = result
    return result
