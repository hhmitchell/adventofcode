import unittest
from . import day18part1


class TestIsIterable(unittest.TestCase):
    def test_list_is_iterable(self):
        self.assertTrue(day18part1.is_iterable([]))

    def test_number_is_not_iterable(self):
        self.assertFalse(day18part1.is_iterable(0))
