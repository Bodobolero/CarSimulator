

# line threshold is a sensor value above 656.6436087300251
SENSOR_LINE_THRESHOLD = 656
SENSOR_MIDDLE_REWARD = 100.0
SENSOR_SIDE_REWARD = 20.0
ON_LINE_BUT_NO_SENSOR = 10.0
LOST_LINE = -300.0
MAX_STEPS = 150


def simpleReward(sensors, position, orientation, carFollowsLine, isTerminated):
    """
    Each reward function receives the current state and returns a float number that
    rewards (positive number) or punishes (negative number) for the state.
    The state includes
    sensors: The 3 sensor values in a list of 3 floating point values: [leftValue, middleValue, rightValue]
    position: The car current position as a tuple of (x,y) coordinates (floating point values).
    orientation: The car current orientation (angle in degrees not radians)
    carFollowsLine: True if the center of the car is approximately on the line
    isTerminated: True if all sensors are outside of the canvas
    """
    if (isTerminated and (not carFollowsLine or position[0] < 500)):
        return MAX_STEPS * -1.0 * SENSOR_MIDDLE_REWARD

    if (isTerminated and carFollowsLine):
        return (MAX_STEPS * SENSOR_MIDDLE_REWARD)

    if (carFollowsLine):
        if (sensors[1] > SENSOR_LINE_THRESHOLD):
            return SENSOR_MIDDLE_REWARD
        if ((sensors[0] > SENSOR_LINE_THRESHOLD) or (sensors[2] > SENSOR_LINE_THRESHOLD)):
            return SENSOR_SIDE_REWARD
        return ON_LINE_BUT_NO_SENSOR
    else:
        if (sensors[1] > SENSOR_LINE_THRESHOLD):
            return SENSOR_MIDDLE_REWARD / 2.0
        if ((sensors[0] > SENSOR_LINE_THRESHOLD) or (sensors[2] > SENSOR_LINE_THRESHOLD)):
            return SENSOR_SIDE_REWARD / 2.0
        return LOST_LINE
