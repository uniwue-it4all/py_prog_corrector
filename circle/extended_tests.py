import math
import unittest
from solution import Circle


class CircleTest(unittest.TestCase):
    unit_circle: Circle = Circle((0, 0), 1)
    circle_2: Circle = Circle((0, 2), 2)
    circle_3: Circle = Circle((5, 3), 3.3)

    def test_init(self):
        circle1: Circle = Circle((3, 6), 2)
        self.assertEqual((3, 6), circle1.center)
        self.assertEqual(2, circle1.radius)

        circle2: Circle = Circle((5, 2), 7)
        self.assertEqual((5, 2), circle2.center)
        self.assertEqual(7, circle2.radius)

    def test_repr(self):
        self.assertEqual('Circle(c = (0, 0), r = 1)', repr(self.unit_circle))
        self.assertEqual('Circle(c = (0, 2), r = 2)', repr(self.circle_2))
        self.assertEqual('Circle(c = (5, 3), r = 3.3)', repr(self.circle_3))

    def test_area(self):
        self.assertAlmostEqual(math.pi, self.unit_circle.area())
        self.assertAlmostEqual(12.566370614359172, self.circle_2.area())
        self.assertAlmostEqual(34.21194399759284, self.circle_3.area())

    def test_perimeter(self):
        self.assertAlmostEqual(2 * math.pi, self.unit_circle.perimeter())
        self.assertAlmostEqual(12.566370614359172, self.circle_2.perimeter())
        self.assertAlmostEqual(20.734511513692635, self.circle_3.perimeter())

    def test_intersects(self):
        self.assertTrue(self.unit_circle.intersects(self.circle_2),
                        "Die Kreise {} und {} sollten sich überschneiden!".format(self.unit_circle, self.circle_2))

        self.assertFalse(self.unit_circle.intersects(self.circle_3),
                         "Die Kreise {} und {} sollten sich nicht überschneiden!".format(
                             self.unit_circle, self.circle_3))
