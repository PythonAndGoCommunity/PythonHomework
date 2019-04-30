from parameterized import parameterized
import unittest
import math
from pycalc.core import *


class TestCheckers(unittest.TestCase):
    def test_check_brackets(self):
        self.assertEqual(check_brackets('()'), None)
        self.assertEqual(check_brackets('()()'), None)

    @parameterized.expand([
        ('wrong side brackets', ')('),
        ('extra opening bracket', '(()'),
        ('extra closing bracket', '())'),
        ('just a mess', '()())))((('),
    ])
    def test_check_brackets_raises(self, name, brackets):
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

    @parameterized.expand([
        ('left associativity', ['1', '+', '2', '+', '3'], [1.0, 2.0, '+', 3.0, '+']),
        ('right associativity', ['1', '+', '2', '^', '3'], [1.0, 2.0, 3.0, '^', '+'])
    ])
    def test_convert_infix_to_postfix(self, name, input, output):
        self.assertEqual(convert_infix_to_postfix(input), output)

    @parameterized.expand([
        ('unexpected operator', OperatorsError, ['+']),
        ('unexpected comma', UnexpectedCommaError, ['(', '12', ',', '12', ')']),
        ('unknown token', UnknownTokensError, ['asdf'])
    ])
    def test_convert_infix_to_postfix_raises(self, name, error, argument):
        with self.assertRaises(error):
            convert_infix_to_postfix(argument)

    @parameterized.expand([
        ('1>=2', (['1', '2'], '>=')),
        ('1', ('1', None)),
    ])
    def test_split_comparison(self, arguments, result):
        self.assertEqual(split_comparison(arguments), result)

    def test_split_comparison_raises(self):   
        with self.assertRaises(OperatorsError):
            split_comparison('1>=2>=3')


class TestEndToEnd(unittest.TestCase):
    @parameterized.expand([
        (calculate([3.0, 2.0, '+']), 5.0),
        (calculate([2.0, 2.0, 2.0, '^', '^']), 16.0),
    ])
    def test_calculate(self, function, result):
        self.assertEqual(function, result)

    def test_calculate_raises(self):
        with self.assertRaises(OperandsError):
            calculate([3.0, 2.0, 1.0, '+'])

    @parameterized.expand([
        (compare(['2', '1'], '>='), ),
        (compare(['1', '2'], '<='), ),
    ])
    def test_compare_true(self, argument):
        self.assertTrue(argument)

    @parameterized.expand([
        (compare(['1', '2'], '>='), ),
        (compare(['2', '1'], '<='), ),
    ])
    def test_compare_false(self, argument):
        self.assertFalse(argument) 

    @parameterized.expand([
        ("simple", "1+2", 3.0),
        ("precedence", "1+2*3", 7.0),
        ("brackets", "(1+2)*3", 9.0),
        ("single argument function", "sin(0)", 0.0),
        ("two argument function", "log(100, 10)", 2.0),
        ("right associativity", "4^3^2", 262144.0),
    ])
    def test_get_result(self, name, expression, result):
        self.assertEqual(get_result(expression), result)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
