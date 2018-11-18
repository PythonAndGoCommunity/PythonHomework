import unittest
import math
from core.calculator import calculator


class TestPycalc(unittest.TestCase):

    def test_implicit_multiplication(self):
        self.assertEqual(calculator('5(5 + 5)', None), 50)

    def test_error(self):
        self.assertTrue(calculator('5 5', None).startswith('ERROR:'))

    def test_priority(self):
        self.assertEqual(calculator('2 + 2 * 2', None), 6)

    def test_functions(self):
        self.assertEqual(calculator('sin(5)', None), math.sin(5))

    def test_constants(self):
        self.assertEqual(calculator('pi + e', None), math.pi + math.e)

    def test_right_associative(self):
        self.assertEqual(calculator('2^4^6', None), 2**4**6)

    def test_multiple_comparison(self):
        self.assertEqual(calculator('5 > 2 > 1', None), 5 > 2 > 1)

    def test_unary_operations(self):
        self.assertEqual(calculator('5--5', None), 5--5)


if __name__ == '__main__':
    unittest.main()
