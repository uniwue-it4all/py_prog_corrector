import unittest
# noinspection PyUnresolvedReferences
from solution import average


class AverageTest(unittest.TestCase):
    def test_average(self):
        self.assertEqual(0, average([0]))
        self.assertAlmostEqual(4., average([3, 4, 5]))
        self.assertAlmostEqual(5.4, average([2, 3, 9, 5, 8]))

        self.assertIsNone(average([]))
