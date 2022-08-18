import RobotCarSimulator
import statistics
import logging
import sys


class HeuristicLineTracker():
    def __init__(self, robot) -> None:
        self._rc = robot
        self._currentSensorValues = []
        self._lineThreshold = 1000
        self._collectedSensorValues = []
        return

    def calibrateAndFindLine(self):
        self._collectedSensorValues = []
        for i in range(5):
            self._currentSensorValues = self._rc.getLineTrackingSensorValues()
            self._collectedSensorValues.extend(self._currentSensorValues)
            self._rc.turnLeft(100, 50)
        for i in range(10):
            self._currentSensorValues = self._rc.getLineTrackingSensorValues()
            self._collectedSensorValues.extend(self._currentSensorValues)
            self._rc.turnRight(100, 50)
        self._rc.turnLeft(100, 200)
        maxValue = max(self._collectedSensorValues)
        standardDeviation = statistics.stdev(self._collectedSensorValues)
        self._lineThreshold = maxValue - (0.75 * standardDeviation)
        self.findLine()

    def findLine(self):
        i = 0
        while (self._currentSensorValues[0] < self._lineThreshold and self._currentSensorValues[1] < self._lineThreshold and self._currentSensorValues[2] < self._lineThreshold):
            self._rc.turnLeft(100, 50)
            self._currentSensorValues = self._rc.getLineTrackingSensorValues()
            i += 1
            if i > 5:
                break
            if (self._rc.isTerminated()):
                return
        i = 0
        while (self._currentSensorValues[0] < self._lineThreshold and self._currentSensorValues[1] < self._lineThreshold and self._currentSensorValues[2] < self._lineThreshold):
            self._rc.turnRight(100, 50)
            self._currentSensorValues = self._rc.getLineTrackingSensorValues()
            i += 1
            if i > 10:
                break
            if (self._rc.isTerminated()):
                return
        if self._currentSensorValues[0] < self._lineThreshold and self._currentSensorValues[1] < self._lineThreshold and self._currentSensorValues[2] < self._lineThreshold:
            raise RuntimeError("Can not find the line")

    def followLine(self):
        while ((self._currentSensorValues[0] > self._lineThreshold) or (self._currentSensorValues[1] > self._lineThreshold) or (self._currentSensorValues[2] > self._lineThreshold)):
            if (self._rc.isTerminated()):
                break
            # line is on the left - turn left
            if self._currentSensorValues[0] > self._lineThreshold:
                print('Turning left with sensor values (L/M/R):' +
                      str(self._currentSensorValues))
                self._rc.turnLeft(100, 50)
                self._currentSensorValues = self._rc.getLineTrackingSensorValues()
                continue
            # line is on the right - turn right
            if self._currentSensorValues[2] > self._lineThreshold:
                print('Turning right with sensor values (L/M/R):' +
                      str(self._currentSensorValues))
                self._rc.turnRight(100, 50)
                self._currentSensorValues = self._rc.getLineTrackingSensorValues()
                continue
            #  straight ahead - line is in middle
            print('Straight ahead with sensor values (L/M/R):' +
                  str(self._currentSensorValues))
            self._rc.driveForward(100, 150)
            self._currentSensorValues = self._rc.getLineTrackingSensorValues()
        print('Leaving follow mode with sensor values:' +
              str(self._currentSensorValues))

    def run(self):
        try:
            self.calibrateAndFindLine()
            while not self._rc.isTerminated():
                self.followLine()
                if (self._rc.isTerminated()):
                    break
                self.findLine()
        except Exception as e:
            print(e, file=sys.stderr)
        return
