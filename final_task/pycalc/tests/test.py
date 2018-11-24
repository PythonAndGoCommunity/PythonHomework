import unittest
import ddt
import math
from pycalc.core.calculator_helper import (
    is_number, may_unary_operator, is_unary_operator,
    check_right_associativity, is_callable, check_brackets_balance,
    check_empty_expression, PycalcError
)

from pycalc.core.calculator import (
    split_operands, implicit_multiplication, may_valid_operation,
    split_arguments, process_func_or_const, final_execution,
    import_modules, execute_comparison, get_length_operator, check_valid_spaces
)


@ddt.ddt
class TestCalculatorHelper(unittest.TestCase):

    @ddt.data('12', '12.5', '12.', '.5')
    def test_is_number_true(self, value):
        self.assertTrue(is_number(value))

    @ddt.data('qwerty', '.')
    def test_is_number_false(self, value):
        self.assertFalse(is_number(value))

    def test_may_unary_operator_true(self):
        self.assertTrue(may_unary_operator('+'))

    def test_may_unary_operator_false(self):
        self.assertFalse(may_unary_operator('^'))

    def test_is_unary_operator_true(self):
        self.assertTrue(is_unary_operator('u+'))

    def test_is_unary_operator_false(self):
        self.assertFalse(is_unary_operator('+'))

    def test_check_right_associativity_true(self):
        self.assertTrue(check_right_associativity('^'))

    def test_is_callable_true(self):
        self.assertTrue(is_callable('sin', math))

    def test_is_callable_false(self):
        self.assertFalse(is_callable('pi', math))

    @ddt.data('(5+3', ')5+3(')
    def test_check_brackets_balance(self, value):
        with self.assertRaises(PycalcError):
            check_brackets_balance(value)

    def test_check_empty_expression(self):
        with self.assertRaises(PycalcError):
            check_empty_expression('')


class TestCalculator(unittest.TestCase):

    def test_split_operands(self):
        self.assertEqual(split_operands('5pie'), ['5', 'pi', 'e'])

    def test_split_operands_raise(self):
        with self.assertRaises(PycalcError):
            split_operands('5abc')

    def test_implicit_multiplication(self):
        self.assertEqual(implicit_multiplication('5pie'), '5*pi*e')

    def test_implicit_multiplication_brackets(self):
        self.assertEqual(implicit_multiplication('(5+5)5'), '(5+5)*5')

    def test_may_valid_operation(self):
        self.assertFalse(may_valid_operation('^', 'u-'))

    def test_split_arguments(self):
        self.assertEqual(split_arguments('5,sin(2),sin(sin(5))'), ['5', 'sin(2)', 'sin(sin(5))'])

    def test_process_func_or_const(self):
        self.assertEqual(process_func_or_const('sin', 'sin(sin(5)+6)', 3, math), (math.sin(math.sin(5) + 6), 12))

    def test_execute_operation(self):
        self.assertEqual(final_execution(['*'], [5, 7]), 35)

    def test_final_execution_comparison(self):
        self.assertTrue(final_execution(['<'], [5, 7]))

    def test_execute_operation_raise(self):
        with self.assertRaises(PycalcError):
            final_execution(['^'], [-5, .5])

    def test_import_modules(self):
        with self.assertRaises(PycalcError):
            import_modules(['module'])

    def test_execute_comparison(self):
        self.assertFalse(execute_comparison([5, 8, 11, 25], ['>', '<', '>=']))

    def test_get_length_operator(self):
        self.assertEqual(get_length_operator('5+5', 1), 1)

    def test_check_valid_spaces(self):
        with self.assertRaises(PycalcError):
            check_valid_spaces('5 5')


if __name__ == '__main__':
    unittest.main()
