import unittest

from average import average


class AverageTest(unittest.TestCase):
    def test_average(self):
        self.assertIsNone(average([]))
        self.assertEqual(1, average([1]))
        self.assertEqual(5, average([3, 5, 7]))


if __name__ == "__main__":
    unittest.main()
