import unittest
from pycalc import add, subtract, multiply, function_from_module_math, calculate, split, parse, divide, \
    comparison, get_whole_part_from_division


class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(subtract(3, 1), 2)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_function_from_module_math(self):
        self.assertEqual(function_from_module_math('cos', 0), 1)
        self.assertEqual(function_from_module_math('sin', 0), 0)
        self.assertEqual(function_from_module_math('tan', 0), 0)
        self.assertEqual(function_from_module_math('exp', 0), 1)
        self.assertEqual(function_from_module_math('abs', -1), 1)
        self.assertEqual(function_from_module_math('log10', 10), 1)
        self.assertEqual(function_from_module_math('round', 4.3), 4)

    def test_parse(self):
        self.assertEqual(parse(['3', '+', '4', '-', 'sin', '(', '5', ')']), [3, 4, '+', 5, 'sin', '-'])

    def test_split(self):
        self.assertEqual(split('3+5-6.6'), ['3', '+', '5', '-', '6.6'])

    def test_calculate(self):
        self.assertEqual(calculate('(6+10-4)/(1+1*2)+1'), 5)

    def test_divide(self):
        self.assertEqual(divide(5, 2), 2.5)

    def test_comparison(self):
        self.assertEqual(comparison('<', 5, 7), True)
        self.assertEqual(comparison('<=', 6, 8), True)
        self.assertEqual(comparison('>', 9, 11), False)
        self.assertEqual(comparison('>=', 15, 17), False)
        self.assertEqual(comparison('!=', 26, 23), True)
        self.assertEqual(comparison('==', 5, 5), True)

    def test_get_whole_part_from_division(self):
        self.assertEqual(get_whole_part_from_division(3, 2), 1)

    if __name__ == '__main__':
        unittest.main()

