import unittest
import logging
import Car
import numpy as np


class TestCar(unittest.TestCase):
    def testCarModel(self):
        car = Car.CarModel(logging.DEBUG)
        self.assertEqual(car._position, (0.0, 0.0))
        self.assertEqual(car._scale, 1.0)
        self.assertEqual(car._rotation, 0.0)

    def testRotateCar(self):
        car = Car.CarModel(logging.DEBUG)
        self.assertEqual(car._rotation, 0.0)
        self.assertEqual(car._position, (0.0, 0.0))
        car.rotate(45.0)
        self.assertEqual(car._rotation, 45.0)
        self.assertEqual(car._position, (0.0, 0.0))
        car.rotate(-15.0)
        self.assertEqual(car._rotation, 30.0)
        self.assertEqual(car._position, (0.0, 0.0))

    def testRotatePoint(self):
        car = Car.CarModel(logging.DEBUG)
        self.assertEqual(car._rotation, 0.0)
        self.assertEqual(car.rotatePoint((10.0, 0)), (10.0, 0))
        self.assertEqual(car.rotatePoint((10.0, 20.0)), (10.0, 20.0))
        self.assertEqual(car.rotatePoint((0.0, 20.0)), (0.0, 20.0))
        self.assertEqual(car.rotatePoint((-10.0, 20.0)), (-10.0, 20.0))
        self.assertEqual(car.rotatePoint((-10.0, 0)), (-10.0, 0))
        self.assertEqual(car.rotatePoint((-10.0, -20.0)), (-10.0, -20.0))

        car.rotate(90.0)
        np.testing.assert_almost_equal(car.rotatePoint((1.0, 0)), (0.0, 1.0))
        np.testing.assert_almost_equal(car.rotatePoint((10.0, 0)), (0, 10.0))
        np.testing.assert_almost_equal(
            car.rotatePoint((10.0, 20.0)), (-20.0, 10.0))
        np.testing.assert_almost_equal(
            car.rotatePoint((0.0, 20.0)), (-20.0, 0.0))
        np.testing.assert_almost_equal(
            car.rotatePoint((-10.0, 20.0)), (-20.0, -10.0))
        np.testing.assert_almost_equal(
            car.rotatePoint((-10.0, 0)), (0.0, -10.0))
        np.testing.assert_almost_equal(
            car.rotatePoint((-10.0, -20.0)), (20.0, -10.0))

    def testMoveCar(self):
        car = Car.CarModel(logging.DEBUG)
        self.assertEqual(car._rotation, 0.0)
        self.assertEqual(car._position, (0.0, 0.0))
        car.moveForward(10.0)
        self.assertEqual(car._rotation, 0.0)
        self.assertEqual(car._position, (10.0, 0.0))
        car.rotate(90.0)
        car.moveForward(20.0)
        np.testing.assert_almost_equal(car._rotation, 90.0)
        np.testing.assert_almost_equal(car._position, (10.0, 20.0))


if __name__ == '__main__':
    unittest.main()
