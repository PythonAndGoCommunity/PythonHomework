import unittest

import math

from .pycalc import (
    get_token,
    parse_to_reverse_polish_notation,
    calculate_expression,
    split_by_comparison,
    comparison_expressions,
    calculate_and_comparison,
    from_str_to_result,
    check_space_between_operands,
    verify_to_elements_operator,
    convert_num_and_const_to_float
    )


#import Exceptions
from .pycalc import (
    WrongBracketsBalance,
    SpaceBetweenOperands,
    SpaceIn2ElementOperators,
    WrongToken,
)


class Test(unittest.TestCase):
    def setUp(self):
        self.expression = get_token('(343+pi^3)/(e+sin(3-11))')
        self.reverse_polish_notation = parse_to_reverse_polish_notation(self.expression)
        self.calculate = calculate_expression(self.reverse_polish_notation)
        self.split_by_comparison_result = split_by_comparison('(343 + pi ^ 3) < (e + sin(3 - 11)) != (845/pi*12^2)')
        self.calculate_and_comparison = calculate_and_comparison(
            *split_by_comparison('(343 + pi ^ 3) < (e + sin(3 - 11)) != (845/pi*12^2)')
        )

    def test_expression_get_token(self):
        self.assertEqual(
            get_token('(343+pi^3)/3(e+sin(3-11))'),
            ['(', '343', '+', 'pi', '^', '3', ')', '/', '3', '(', 'e', '+', 'sin', '(', '3', '-11', ')', ')']
        )

    def test_expression_get_token_with_unary(self):
        self.assertEqual(
            get_token('-343+pi^3'),
            ['-343', '+', 'pi', '^', '3']
        )

    def test_expression_get_token_with_duble_minus(self):
        self.assertEqual(
            get_token('--343+pi^3'),
            ['+', '343', '+', 'pi', '^', '3']
        )

    def test_expression_polish_notation(self):
        rpn = parse_to_reverse_polish_notation(get_token('(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)'))
        self.assertEqual(
            rpn,
            [2.0, 3.141592653589793, 3.141592653589793, '/', 2.718281828459045, 2.718281828459045,
             '/', '+', 2.0, 0.0, '^', '+', '^', 1.0, 3.0, '/', '^']
        )


    def test_from_string_co_result(self):
        self.assertEqual(from_str_to_result('--343+pi^3'), (--343+math.pi**3))

    def test_calculate_expr(self):
        self.assertEqual(
            self.calculate,
            216.3231970514297
        )

    def test_check_for_negativ_and_constants(self):
        self.assertEqual(convert_num_and_const_to_float(['(', '-1', '+', '5,0', '+', 'pi', ')']),
                         ['(', -1.0, '+', 5.0, '+', math.pi,  ')'])

    def test_split_by_comparison(self):
        self.assertEqual(
            self.split_by_comparison_result,
            (['(343+pi^3)', '(e+sin(3-11))', '(845/pi*12^2)'], ['<', '!='])
        )

    def test_calculate_and_comparison(self):
        self.assertFalse(
            self.calculate_and_comparison
        )

    def test_comparison_eq(self):
        self.assertTrue(
            comparison_expressions([5, 5], ['=='])
        )

    def test_comparison_ge(self):
        self.assertTrue(
            comparison_expressions([8, 5], ['>='])
        )

    def test_comparison_le(self):
        self.assertTrue(
            comparison_expressions([5, 8], ['<='])
        )

    def test_comparison_ne_true(self):
        self.assertTrue(
            comparison_expressions([5, 8], ['!='])
        )

    def test_comparison_ne_false(self):
        self.assertFalse(
            comparison_expressions([5, 5], ['!='])
        )

    def test_from_str_to_result(self):
        self.assertEqual(from_str_to_result('(2.0^(pi/pi+e/e+2.0^0.0))'), 8)

    def test_error_raising_brackets(self):
        with self.assertRaises(WrongBracketsBalance):
            from_str_to_result('((1+15)')

    def test_error_raising_space_between_operands(self):
        with self.assertRaises(SpaceBetweenOperands):
            check_space_between_operands("1 + 1 2 3 4 5 6 ")

    def test_error_raising_space_2el_operators(self):
        with self.assertRaises(SpaceIn2ElementOperators):
            verify_to_elements_operator('6 < = 6')

    def test_wrong_token(self):
        with self.assertRaises(WrongToken):
            parse_to_reverse_polish_notation(['(', '-1', '+', '5', '+', 'qwe', ')'])

    def test_zero_divizion(self):
        self.failureException(calculate_expression([ '0', '5.0', '/']), ZeroDivisionError)

