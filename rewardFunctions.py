

# line threshold is a sensor value above 656.6436087300251
SENSOR_LINE_THRESHOLD = 656
SENSOR_MIDDLE_REWARD = 100.0
SENSOR_SIDE_REWARD = 20.0
ON_LINE_BUT_NO_SENSOR = 10.0
LOST_LINE = -300.0
MAX_STEPS = 150
MAX_SECONDS = 60.0


def simpleReward(time, sensors, position, orientation, carFollowsLine, isTerminated):
    """
    Each reward function receives the current state and returns a float number that
    rewards (positive number) or punishes (negative number) for the state.
    The state includes
    time: seconds (floating point) since the experiment started
    sensors: The 3 sensor values in a list of 3 floating point values: [leftValue, middleValue, rightValue]
    position: The car current position as a tuple of (x,y) coordinates (floating point values).
    orientation: The car current orientation (angle in degrees not radians)
    carFollowsLine: True if the center of the car is approximately on the line
    isTerminated: True if all sensors are outside of the canvas
    """
    if (isTerminated and not carFollowsLine):
        return MAX_STEPS * -1.0 * SENSOR_MIDDLE_REWARD

    if (isTerminated and carFollowsLine):
        # assumes that 60 seconds is max time we need
        return (MAX_STEPS * SENSOR_MIDDLE_REWARD) * (max(MAX_SECONDS - time, 0.0)/MAX_SECONDS)

    if (carFollowsLine):
        if (sensors[1] > SENSOR_LINE_THRESHOLD):
            return SENSOR_MIDDLE_REWARD * (max(MAX_SECONDS - time, 0.0)/MAX_SECONDS)
        if ((sensors[0] > SENSOR_LINE_THRESHOLD) or (sensors[2] > SENSOR_LINE_THRESHOLD)):
            return SENSOR_SIDE_REWARD * (max(MAX_SECONDS - time, 0.0)/MAX_SECONDS)
        return ON_LINE_BUT_NO_SENSOR * (max(MAX_SECONDS - time, 0.0)/MAX_SECONDS)
    else:
        if (sensors[1] > SENSOR_LINE_THRESHOLD):
            return SENSOR_MIDDLE_REWARD / 2.0 * (max(MAX_SECONDS - time, 0.0)/MAX_SECONDS)
        if ((sensors[0] > SENSOR_LINE_THRESHOLD) or (sensors[2] > SENSOR_LINE_THRESHOLD)):
            return SENSOR_SIDE_REWARD / 2.0 * (max(MAX_SECONDS - time, 0.0)/MAX_SECONDS)
        return LOST_LINE
