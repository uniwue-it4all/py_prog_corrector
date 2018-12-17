import unittest
from typing import List


def average(my_list: List[int]) -> float:
    length = len(my_list)
    if length == 0:
        return "Fehler"
    else:
        return sum(my_list) / length


class AverageTest(unittest.TestCase):
    def test_average(self):
        self.assertEqual(0, average([0]))
        self.assertAlmostEqual(4., average([3, 4, 5]))
        self.assertAlmostEqual(5.4, average([2, 3, 9, 5, 8]))

        with self.assertRaises(Exception):
            average([])
