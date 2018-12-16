"""Unittest for module preprocessing."""

import unittest

from collections import namedtuple

from pycalc_src.preprocessing import (preprocessing,
                                      _is_operators_available,
                                      _clean_repeatable_operators)
from pycalc_src.exceptions import BaseCalculatorException


class TestStringMethods(unittest.TestCase):
    """Docstring."""

    def test_preprocessing__valid_expressions(self):
        """Docstring."""
        valid_expression = namedtuple('valid_expression', 'expression result')
        valid_expressions = [valid_expression('TAN(1)', 'tan(1)'),
                             valid_expression('**', '^')
                             ]

        for expression in valid_expressions:
            func_result = preprocessing(expression.expression)

            self.assertEqual(func_result, expression.result)

    def test_preprocessing__invalid_expressions(self):
        """Docstring."""

        invalid_expression = namedtuple('valid_expression', 'expression')
        invalid_expressions = [invalid_expression(''),
                               invalid_expression(set()),
                               invalid_expression('(()'),
                               ]

        for expression in invalid_expressions:
            with self.assertRaises(BaseCalculatorException):
                result = preprocessing(expression.expression)

    def test_preprocessing__valid_expressions(self):
        """Docstring."""
        valid_expression = namedtuple('valid_expression', 'expression result')
        valid_expressions = [valid_expression('--1', '+1'),
                             valid_expression('-+2', '-2'),
                             valid_expression('++2.4', '+2.4'),
                             valid_expression('-+-+-++++------3', '-3')
                             ]

        for expression in valid_expressions:
            func_result = _clean_repeatable_operators(expression.expression)

            self.assertEqual(func_result, expression.result)


if __name__ == '__main__':
    unittest.main()
