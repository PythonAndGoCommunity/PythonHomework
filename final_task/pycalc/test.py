from parameterized import parameterized
import unittest
import math
from pycalc.core import *


class TestCheckers(unittest.TestCase):
    @parameterized.expand([
        ('wrong side brackets', ')('),
        ('extra opening bracket', '(()'),
        ('extra closing bracket', '())'),
        ('just a mess', '()())))((('),
    ])
    def test_check_brackets(self, name, brackets):
        self.assertEqual(check_brackets('()'), None)
        with self.assertRaises(UnbalancedBracketsError):
            check_brackets(brackets)

    @parameterized.expand([
        ('numbers', '12 34'),
        ('numbers with dots', '12. 34'),
        ('comparison operator', '< ='),
        ('floor division', '/ /'),
        ('power', '* *'),
    ])
    def test_check_whitespace(self, name, whitespace):
        with self.assertRaises(WhitespaceError):
            check_whitespace(whitespace)

    @parameterized.expand([
        ('function', 'sin(1, 2)'),
        ('on its own', ','),
    ])
    def test_check_commas(self, name, comma):
        with self.assertRaises(UnexpectedCommaError):
            check_commas(comma)


class TestCoreFunctions(unittest.TestCase):
    def test_get_tokens(self):
        self.assertEqual(get_tokens('1+2+3'), ['1', '+', '2', '+', '3'])
        with self.assertRaises(EmptyExpressionError):
            get_tokens('')

    def test_convert_infix_to_postfix(self):
        self.assertEqual(convert_infix_to_postfix(['1', '+', '2', '+', '3']), [1.0, 2.0, '+', 3.0, '+'])
        self.assertEqual(convert_infix_to_postfix(['1', '+', '2', '^', '3']), [1.0, 2.0, 3.0, '^', '+'])
        with self.assertRaises(OperatorsError):
            convert_infix_to_postfix(['+'])
        with self.assertRaises(UnexpectedCommaError):
            convert_infix_to_postfix(['(', '12', ',', '12', ')'])
        with self.assertRaises(UnknownTokensError):
            convert_infix_to_postfix(['asdf'])

    def test_split_comparison(self):
        self.assertEqual(split_comparison('1>=2'), (['1', '2'], '>='))
        self.assertEqual(split_comparison('1'), ('1', None))
        with self.assertRaises(OperatorsError):
            split_comparison('1>=2>=3')

    def test_calculate(self):
        self.assertEqual(calculate([3.0, 2.0, '+']), 5.0)
        self.assertEqual(calculate([2.0, 2.0, 2.0, '^', '^']), 16.0)
        with self.assertRaises(OperandsError):
            calculate([3.0, 2.0, 1.0, '+'])

    def test_get_result(self):
        self.assertEqual(get_result('1+4'), 5.0)

    def test_compare(self):
        self.assertTrue(compare(['2', '1'], '>='))
        self.assertFalse(compare(['1', '2'], '>='))


if __name__ == '__main__':
    unittest.main()
