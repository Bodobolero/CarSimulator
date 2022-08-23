# CarSimulator
Car simulator to try reinforcement learning of line tracking with Arduino Robo Car

Note:

the reason why curve with seed 7 currently fails is that the simulator does not put the car in a correct 
starting position: the infrared sensors are not correctly placed on the line because the line has a curve quite close to the starting point.
This exception was never encountered while training and can not be treated well if the
only information known to the model is the sensor values - if all sensors are placed on the white canvas
even a human being (without further information) would not be able to navigte correctly.
I consider this rather a current limitation of the simulator init() code rather than a problem in the model.
