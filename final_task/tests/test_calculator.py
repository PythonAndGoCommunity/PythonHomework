"""Unittest for class Calculator."""

import unittest

import operator
import builtins
import math

from collections import namedtuple

from pycalc_src.calculator import Calculator
from pycalc_src.exceptions import BaseCalculatorException


class TestStringMethods(unittest.TestCase):
    """Docstring."""

    def test_process_digit__valid_expressions(self):
        """Docstring."""
        valid_expression = namedtuple('valid_expression', 'expression index symbol result')
        valid_expressions = [valid_expression('5', 0, '5', '5'),
                             valid_expression(' .', 1, '.', '.'),
                             valid_expression('1 ', 0, '1', '1')
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)
            calc._process_digit(expression.index, expression.symbol)

            self.assertEqual(calc.number, expression.result)

    def test_process_digit__invalid_expressions(self):
        """Docstring."""

        expression = '1 2 3 4'

        calc = Calculator(expression)
        calc._Calculator__return_code = 0
        calc.number = '1'

        with self.assertRaises(BaseCalculatorException):
            calc._process_digit(2, '2')

    def test_process_number_and_constant__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'unary_operator number operator result')
        valid_expressions = [valid_expression('', '54.55', '', 54.55),
                             valid_expression('-@', '5', '', -5),
                             valid_expression('', '', 'pi', math.pi),
                             valid_expression('-@', '', 'e', -math.e)
                             ]

        for expression in valid_expressions:
            calc = Calculator('')
            calc.unary_operator = expression.unary_operator
            calc.number = expression.number
            calc.operator = expression.operator
            calc._process_number_and_constant()

            self.assertEqual(calc.rpn[-1], expression.result)

    def test_process_operator__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'unary_operator operator closing_bracket_index result')
        valid_expressions = [valid_expression('', 'sin', 2, ['sin']),
                             valid_expression('-@', 'log', 2, ['-@', 'log'])
                             ]

        for expression in valid_expressions:
            calc = Calculator('')
            calc.unary_operator = expression.unary_operator
            calc.operator = expression.operator
            calc._process_operator(expression.closing_bracket_index)

            self.assertEqual(calc.stack, expression.result)

    def test_process_operator__invalid_expressions(self):
        """Docstring."""

        invalid_expression = namedtuple('valid_expression', 'unary_operator operator closing_bracket_index')
        invalid_expressions = [invalid_expression('', 'log100', 0),
                               invalid_expression('-@', 'sin4', 0)
                               ]

        for expression in invalid_expressions:
            calc = Calculator('')
            calc._Calculator__return_code = 0
            calc.unary_operator = expression.unary_operator
            calc.operator = expression.operator

            with self.assertRaises(BaseCalculatorException):
                calc._process_operator(expression.closing_bracket_index)

    def test_process_stack__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'stack symbol result_stack result_rpn')
        valid_expressions = [valid_expression(['^'], '^', ['^', '^'], []),
                             valid_expression(['*'], '+', ['+'], ['*']),
                             valid_expression(['-'], '/', ['-', '/'], []),
                             valid_expression(['sin', 'tan'], '/', ['/'], ['tan', 'sin'])
                             ]

        for expression in valid_expressions:
            calc = Calculator('')
            calc.stack = expression.stack
            calc._process_stack(expression.symbol)

            self.assertEqual(calc.stack, expression.result_stack)
            self.assertEqual(calc.rpn, expression.result_rpn)

    def test_process_comparison__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression stack index symbol result_stack result_rpn')
        valid_expressions = [valid_expression('5 >= 4', ['>'], 3, '=', ['>='], []),
                             valid_expression('5+1*2 > 4', ['+', '*'], 7, '>', ['>'], ['*', '+'])
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)
            calc.stack = expression.stack
            calc._process_comparison(expression.index, expression.symbol)

            self.assertEqual(calc.stack, expression.result_stack)
            self.assertEqual(calc.rpn, expression.result_rpn)

    def test_process_comparison__invalid_expressions(self):
        """Docstring."""

        invalid_expression = namedtuple('invalid_expression', 'expression stack index symbol')
        invalid_expressions = [invalid_expression('5 > = 4', ['>'], 4, '='),
                               invalid_expression('5+2 = = 4', ['='], 6, '=')
                               ]

        for expression in invalid_expressions:
            calc = Calculator(expression.expression)
            calc._Calculator__return_code = 0
            calc.stack = expression.stack

            with self.assertRaises(BaseCalculatorException):
                calc._process_comparison(expression.index, expression.symbol)

    def test_process_brackets_and_comma__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'stack index symbol number result_stack result_rpn')
        valid_expressions = [valid_expression(['round', '('], 0, ',', '', ['round', '(', ','], []),
                             valid_expression(['round', '(', '+'], 0, ',', '', ['round', '(', ','], ['+']),
                             valid_expression(['+'], 0, '(', '', ['+', '('], []),
                             valid_expression(['+'], 0, '(', '2', ['+', '*', '('], [2]),
                             valid_expression(['(', '+', '*'], 0, ')', '', [], ['*', '+']),
                             valid_expression(['+', '(', '*'], 0, ')', '', ['+'], ['*'])
                             ]

        for expression in valid_expressions:
            calc = Calculator('expression')
            calc.stack = expression.stack
            calc.number = expression.number
            calc._process_brackets_and_comma(expression.index, expression.symbol)

            self.assertEqual(calc.stack, expression.result_stack)
            self.assertEqual(calc.rpn, expression.result_rpn)

    def test_is_unary_operator__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression index symbol result')
        valid_expressions = [valid_expression('-4', 0, '-', True),
                             valid_expression('- 4', 0, '-', True),
                             valid_expression('!4', 0, '!', False),
                             valid_expression('-4', 4, '-', False),
                             valid_expression('1*-4', 2, '-', True),
                             valid_expression('(1*2)-4', 5, '-', False),
                             valid_expression('5==-5', 3, '-', True)
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)
            func_result = calc._is_unary_operator(expression.index, expression.symbol)

            if expression.result:
                self.assertTrue(func_result)
            else:
                self.assertFalse(func_result)

    def test_is_floordiv__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression index symbol result')
        valid_expressions = [valid_expression('5/5', 4, '', False),
                             valid_expression('4//3', 2, '/', True),
                             valid_expression('4/3', 1, '/', False)
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)
            func_result = calc._is_floordiv(expression.index, expression.symbol)

            if expression.result:
                self.assertTrue(func_result)
            else:
                self.assertFalse(func_result)

    def test_process_expression__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression result_rpn')
        valid_expressions = [valid_expression('pi', [3.141592653589793]),
                             valid_expression('<=', ['<=']),
                             valid_expression('log2()', ['log2']),
                             valid_expression('51.567', [51.567]),
                             valid_expression('round(1.233333, 2)', [1.233333, 2, ',', 'round']),
                             valid_expression('81//8', [81, 8, '//']),
                             valid_expression('//', ['//']),
                             valid_expression('-100', [-100]),
                             valid_expression('pi*log2(1)==-1', [3.141592653589793, 1, 'log2', '*', -1, '=='])
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)
            calc._process_expression()

            self.assertEqual(calc.rpn, expression.result_rpn)

    def test_process_expression__invalid_expressions(self):
        """Docstring."""

        invalid_expression = namedtuple('invalid_expression', 'expression')
        invalid_expressions = [invalid_expression('not an expression')
                               ]

        for expression in invalid_expressions:
            calc = Calculator(expression.expression)
            calc._Calculator__return_code = 0

            with self.assertRaises(BaseCalculatorException):
                calc._process_expression()

    def test_calculate_operator__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression stack operator result_stack')
        valid_expressions = [valid_expression('1+2', [1, 2], '+', [3]),
                             valid_expression('round(1.2254,2)', [1.2254, 2, ','], 'round', [1.23]),
                             valid_expression('log(.5)', [0.5], 'log', [-0.6931471805599453])
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)
            calc.stack = expression.stack
            calc._calculate_operator(expression.operator)

            self.assertEqual(calc.stack, expression.result_stack)

    def test_calculate_operator__invalid_expressions(self):
        """Docstring."""

        invalid_expression = namedtuple('invalid_expression', 'expression stack operator')
        invalid_expressions = [invalid_expression('log(.5,)', [0.5, ','], 'log'),
                               invalid_expression('log(.5,1,2)', [0.5, 1, 2, ',', ','], 'log')
                               ]

        for expression in invalid_expressions:
            calc = Calculator(expression.expression)
            calc._Calculator__return_code = 0
            calc.stack = expression.stack

            with self.assertRaises(BaseCalculatorException):
                calc._calculate_operator(expression.operator)

    def test_calculate_result__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression',
                                      'expression function first_operand second_operand result_stack')
        valid_expressions = [valid_expression('365+635', operator.add, 365, 635, [1000]),
                             valid_expression('sin(1)', math.sin, 1, None, [0.8414709848078965])
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)
            calc._calculate_result(expression.function, expression.first_operand, expression.second_operand)

            self.assertEqual(calc.stack, expression.result_stack)

    def test_calculate_result__invalid_expressions(self):
        """Docstring."""

        invalid_expression = namedtuple('invalid_expression', 'expression function first_operand second_operand')
        invalid_expressions = [invalid_expression('5/0', operator.truediv, 5, 0),
                               invalid_expression('log(-100)', math.log, -100, None),
                               invalid_expression('log(1,,)', math.log, 1, ',')
                               ]

        for expression in invalid_expressions:
            calc = Calculator(expression.expression)
            calc._Calculator__return_code = 0

            with self.assertRaises(BaseCalculatorException):
                calc._calculate_result(expression.function, expression.first_operand, expression.second_operand)

    def test_calculate_rpn__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression rpn result_stack')
        valid_expressions = [valid_expression(',', [','], [',']),
                             valid_expression('-(3)', [3, '-@'], [-3]),
                             valid_expression('1+cos(1)', [1, 1, 'cos', '+'], [1.5403023058681398]),
                             valid_expression('1563', [1563], [1563])
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)
            calc.rpn = expression.rpn
            calc._calculate_rpn()

            self.assertEqual(calc.stack, expression.result_stack)

    def test_replace_unary_operator__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'unary_operator result')
        valid_expressions = [valid_expression('-@', '-'),
                             valid_expression('+@', '+')
                             ]

        for expression in valid_expressions:
            calc = Calculator('expression')

            result = calc._replace_unary_operator(expression.unary_operator)

            self.assertEqual(result, expression.result)

    def test_convert_to_number__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'number result')
        valid_expressions = [valid_expression('569', 569),
                             valid_expression('789.99', 789.99),
                             valid_expression('-500.87', -500.87),
                             valid_expression([], 0)
                             ]

        for expression in valid_expressions:
            calc = Calculator('expression')

            result = calc._convert_to_number(expression.number)

            self.assertEqual(result, expression.result)

    def test_process_implicit_multiplication__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression index result_stack')
        valid_expressions = [valid_expression('(1)(1+2)', 3, ['*'])
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)

            calc._process_implicit_multiplication(expression.index)

            self.assertEqual(calc.stack, expression.result_stack)

    def test_get_previous_symbol__valid_expressions(self):
        """Docstring."""

        valid_expression = namedtuple('valid_expression', 'expression index result')
        valid_expressions = [valid_expression('1 +  2', 5, '+')
                             ]

        for expression in valid_expressions:
            calc = Calculator(expression.expression)

            result = calc._get_previous_symbol(expression.index)

            self.assertEqual(result, expression.result)


if __name__ == '__main__':
    unittest.main()
