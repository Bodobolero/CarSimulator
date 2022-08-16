#!/usr/bin/env python3

"""
module that provides a simulator API for the smart Robot car

@author Peter Bendel
Copyright 2021 Peter Bendel, see LICENSE file
"""

import logging


class SimulatorControl():

    def __init__(self, canvas, logLevel=logging.INFO) -> None:
        """ By default the simulator will log to stderr with log level INFO.
        The module uses log levels INFO for major events and DEBUG for debugging.
        """
        self.__configLogger(logLevel)
        self._canvas = canvas
        return

    def getLineTrackingSensorValues(self):
        """ Retrieve the Infrared sensor values of the three infrared sensors on the bottom of the car used for line tracking.
        The list returned contains (in driving direction) the values
        [leftValue, middleValue, rightValue]
        The values vary approximately between 0 and 1000 where lower value indicates lighter ground and higher values indicates
        darker ground
        """
        # TODO
        listOfInts = [500, 500, 500]
        self._logger.info(f'Infrared sensor values (L/M/R): {listOfInts}')
        return listOfInts

    def driveForward(self, speed=160, duration=1000):
        """ Synchronous command to drive forward.
        This command returns when the movement duration finishes.
        *speed* is a value from 0-255; int; default 160
        *duration* in milli-seconds; int; default 1000
        """
        # TODO
        return

    def turnLeft(self, speed=160, duration=400):
        """ Synchronous command to turn left.
        This command returns when the movement duration finishes.
        *speed* is a value from 0-255; int; default 160
        *duration* in milli-seconds; int; default 400
        """
        # TODO
        return

    def turnRight(self, speed=160, duration=400):
        """ Synchronous command to turn right.
        This command returns when the movement duration finishes.
        *speed* is a value from 0-255; int; default 160
        *duration* in milli-seconds; int; default 400
        """
        # TODO
        return
