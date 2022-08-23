#!/usr/bin/env python3

"""
module that provides a simulator API for the smart Robot car

@author Peter Bendel
Copyright 2021 Peter Bendel, see LICENSE file
"""

import logging
import Car
import Canvas
import RobotCarSimulator
import Heuristic
import pprint
import sys
from PIL import ImageFont
from rewardFunctions import simpleReward
from collections import deque

genevafont = ImageFont.truetype("Geneva.ttf", 30)


class SimulatorControl():

    def __init__(self, canvas, car, createGif=True, rewardFunction=simpleReward, logLevel=logging.INFO, stephistory=2) -> None:
        """ By default the simulator will log to stderr with log level INFO.
        The module uses log levels INFO for major events and DEBUG for debugging.

        If you want to create an animated gif of this experiment set createGif to True.
        To save resources if gif is not needed set createGif=False
        stephistory: keeps sensorvalues for stephistory generations in memory
        """
        self.__configLogger(logLevel)
        self._canvas = canvas
        self._car = car
        self._reward = 0.0
        self._previousRewardPositions = set()
        self._xmax = 0
        self._rewardFunction = rewardFunction
        self._time = 0.0
        self._isTerminated = False
        self._followsLine = True
        self._canvasPoints = self._canvas.getCanvasBoundingPoints()
        self._curvePoints = self._canvas.getCurveBoundingPoints()
        car.setPosition(canvas.getCurveStartingPoint())
        # TODO: this orientation does not guarantee to place the sensors on the line
        # for example for curve with seed 7 all sensors are on the white canvas
        car.setOrientation(canvas.getCurveStartingOrientation())
        self._carPositions = []
        self._carOrientations = []
        self._actionLog = []
        self._images = []
        self._durations = []
        self._createGif = createGif
        self._sensorValues = []
        self._previousSensorValues = deque(maxlen=(stephistory*3))
        self.logCar("init", None, 100)
        for i in range(stephistory):
            self._previousSensorValues.extend(self._sensorValues)
        return

    def logCar(self, actionname, actionparms, duration):
        self._updateLineTrackingSensorValues()
        self._followsLine = self._car.followsLine(self._curvePoints)
        self._isTerminated = not self._car.isAtLeastOneCarSensorWithinBounds(
            self._canvasPoints)
        self._actionLog.append((actionname, actionparms, duration))
        self._carPositions.append(self._car._position)
        self._carOrientations.append(self._car._rotation)
        self._time += duration/1000
        position = (round(self._car._position[0], 2), round(self._car._position[1], 2), round(self._car._rotation, 2),
                    self._followsLine, self._isTerminated)
        newx = self._car._position[0]
        if (newx > self._xmax):
            self._xmax = newx
        # no reward for going to the left (all curves go the right) or for reaching same position as before
        if (position in self._previousRewardPositions or newx < self._xmax):
            self._reward = 0.0
        else:
            self._previousRewardPositions.add(position)
            self._reward = self._rewardFunction(
                self._sensorValues, self._car._position, self._car._rotation, self._followsLine, self._isTerminated)
        self.addImageWithDuration(duration)
        self._logger.debug(
            f'Sim: {actionname}: {actionparms}, duration {duration}, new pos: {self._car._position}, new angle: {self._car._rotation}, reward: {self._reward}')
        return

    def addImageWithDuration(self, duration):
        if (self._createGif):
            self._durations.append(duration)
            (img, draw) = self._canvas.createImageAndDraw()
            self._car.draw(draw)
            text = 'Step: {:3d} Time: {:.2f} s - Sensors: L {:.0f} M {:.0f} R {:.0f} - Reward: {:.0f}'.format(len(self._images), self._time,
                                                                                                              self._sensorValues[0], self._sensorValues[1], self._sensorValues[2], self._reward)
            draw.text((400, 50), text, font=genevafont)
            self._images.append(img)
            self._durations.append(duration)
        return

    def _updateLineTrackingSensorValues(self):
        """ Retrieve the Infrared sensor values of the three infrared sensors on the bottom of the car used for line tracking.
        The list returned contains (in driving direction) the values
        [leftValue, middleValue, rightValue]
        The values vary approximately between 0 and 1000 where lower value indicates lighter ground and higher values indicates
        darker ground
        """
        listOfFloats = self._car.computeSensorValues(self._curvePoints)
        self._logger.debug(f'Infrared sensor values (L/M/R): {listOfFloats}')
        self._previousSensorValues.extend(self._sensorValues)
        self._sensorValues = listOfFloats
        return listOfFloats

    def getLineTrackingSensorValues(self):
        return self._sensorValues

    def getPreviousLineTrackingSensorValues(self):
        return self._previousSensorValues

    def getDuration(self):
        return self._time

    def driveForward(self, speed=100, duration=1000):
        """ Synchronous command to drive forward.
        This command returns when the movement duration finishes.
        *speed* is a value from 0-255; int; default 160
        TODO: currently we only support the default speed of 100
        *duration* in milli-seconds; int; default 1000
        """
        distance_in_mm = 0.29 * duration - 10.59
        self._car.moveForward(distance_in_mm)

        self.logCar("driveForward", speed, duration)
        return

    def turnLeft(self, speed=100, duration=400):
        """ Synchronous command to turn left.
        This command returns when the movement duration finishes.
        *speed* is a value from 0-255; int; default 160
        TODO: currently we only support the default speed of 100
        *duration* in milli-seconds; int; default 400
        """
        rotation_angle = -1.0*(0.14 * duration - 2.75)
        self._car.rotate(rotation_angle)
        self.logCar("turnLeft", speed, duration)
        return

    def turnRight(self, speed=160, duration=400):
        """ Synchronous command to turn right.
        This command returns when the movement duration finishes.
        *speed* is a value from 0-255; int; default 160
        *duration* in milli-seconds; int; default 400
        """
        rotation_angle = 0.14 * duration - 2.75
        self._car.rotate(rotation_angle)
        self.logCar("turnRight", speed, duration)
        return

    def isTerminated(self):
        """
        if all sensors are outside of the canvas we stop the simulation
        also if we have reached the right end of the canvas
        """
        return self._isTerminated

    def carFollowsLine(self):
        """True if the center of the car is approximately on the line
        """
        return self._followsLine

    def getReward(self):
        return self._reward

    def saveImage(self, file='carsimulation.gif'):
        """
        file: create an animated gif and save it under path given
        works only if createGif=True
        """
        if (self._createGif):
            self._images[0].save(file, format='GIF', append_images=self._images[1:],
                                 save_all=True, duration=self._durations, loop=0, optimize=True)

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

    def runModelAndSaveVideo(self, modelfile, videofile, seed=5, logLevel=logging.INFO):
        # TODO
        return

    if __name__ == '__main__':
        seed = 5
        if (len(sys.argv) > 1):
            seed = int(sys.argv[1])
        car = Car.CarModel(logLevel=logging.DEBUG)
        canvas = Canvas.CanvasModel(seed=seed, logLevel=logging.DEBUG)
        sim = RobotCarSimulator.SimulatorControl(
            canvas, car, createGif=True, logLevel=logging.DEBUG)
        heuristic = Heuristic.HeuristicLineTracker(sim)
        heuristic.run()
        sim.saveImage('heuristic_seed_{}.gif'.format(seed))
        with open('heuristic_seed_{}.txt'.format(seed), 'w') as f:
            f.write("actions:\n")
            f.write(pprint.pformat(sim._actionLog))
            f.write("\n\npositions:\n")
            f.write(pprint.pformat(sim._carPositions))
            f.write("\n\norientations:\n")
            f.write(pprint.pformat(sim._carOrientations))
        exit(0)
