"""Unittest for module preprocessing."""

import unittest

from collections import namedtuple

from pycalc_src.preprocessor import Preprocessor
from pycalc_src.exceptions import BaseCalculatorException

RETURN_CODE = 0


class TestStringMethods(unittest.TestCase):
    """Docstring."""

    def test_prepare_expression__valid_expressions(self):
        """Docstring."""
        valid_expression = namedtuple('valid_expression', 'expression result')
        valid_expressions = [valid_expression('TAN(1)', 'tan(1)'),
                             valid_expression('**', '^')
                             ]

        for expression in valid_expressions:
            preprocessor = Preprocessor(expression.expression)
            func_result = preprocessor.prepare_expression()

            self.assertEqual(func_result, expression.result)

    def test_preprocessing__invalid_expressions(self):
        """Docstring."""

        invalid_expression = namedtuple('valid_expression', 'expression')
        invalid_expressions = [invalid_expression(''),
                               invalid_expression(set()),
                               invalid_expression('(()'),
                               ]

        for expression in invalid_expressions:
            preprocessor = Preprocessor(expression.expression)
            preprocessor._return_code = RETURN_CODE

            with self.assertRaises(BaseCalculatorException):
                result = preprocessor.prepare_expression()

    def test_clean_repeatable_operators__valid_expressions(self):
        """Docstring."""
        valid_expression = namedtuple('valid_expression', 'expression result')
        valid_expressions = [valid_expression('--1', '+1'),
                             valid_expression('-+2', '-2'),
                             valid_expression('++2.4', '+2.4'),
                             valid_expression('-+-+-++++------3', '-3'),
                             valid_expression('-+-3++', '+3+')
                             ]

        for expression in valid_expressions:
            preprocessor = Preprocessor(expression.expression)
            preprocessor._clean_repeatable_operators()

            self.assertEqual(preprocessor.expression, expression.result)


if __name__ == '__main__':
    unittest.main()
