import unittest
import math
from pycalc.core import *


class TestCalc(unittest.TestCase):
    def test_check_brackets(self):
        with self.assertRaises(ErrorBracketsBalance):
            check_brackets('())')

    def test_check_whitespace(self):
        with self.assertRaises(ErrorWhitespace):
            check_whitespace('1  2')

    def test_check_commas(self):
        with self.assertRaises(ErrorUnexpectedComma):
            check_commas(',')

    def test_get_tokens(self):
        self.assertEqual(get_tokens('1+2+3'), ['1', '+', '2', '+', '3'])
        with self.assertRaises(ErrorEmptyExpression):
            get_tokens('')

    def test_infix_to_postfix(self):
        self.assertEqual(infix_to_postfix(['1', '+', '2', '+', '3']), [1.0, 2.0, '+', 3.0, '+'])
        self.assertEqual(infix_to_postfix(['1', '+', '2', '^', '3']), [1.0, 2.0, 3.0, '^', '+'])
        with self.assertRaises(ErrorOperators):
            infix_to_postfix(['+'])
        with self.assertRaises(ErrorUnexpectedComma):
            infix_to_postfix(['(', '12', ',', '12', ')'])
        with self.assertRaises(ErrorUnknownTokens):
            infix_to_postfix(['asdf'])

    def test_split_comparison(self):
        self.assertEqual(split_comparison('1>=2'), (['1', '2'], '>='))
        self.assertEqual(split_comparison('1'), ('1', None))
        with self.assertRaises(ErrorOperators):
            split_comparison('1>=2>=3')

    def test_calculate(self):
        self.assertEqual(calculate([3.0, 2.0, '+']), 5.0)
        self.assertEqual(calculate([2.0, 2.0, 2.0, '^', '^']), 16.0)
        with self.assertRaises(ErrorOperands):
            calculate([3.0, 2.0, 1.0, '+'])

    def test_get_result(self):
        self.assertEqual(get_result('1+4'), 5.0)

    def test_compare(self):
        self.assertTrue(compare(['2', '1'], '>='))
        self.assertFalse(compare(['1', '2'], '>='))


if __name__ == '__main__':
    unittest.main()
