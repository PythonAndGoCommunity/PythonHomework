from unittest import TestCase
from calculator import pycalc
import math


class TestRPN(TestCase):
    def setUp(self):
        self.rpn = pycalc.RPN()

    def test_clear_stack(self):
        self.rpn.stack = ['3', '2', '*']
        self.rpn.stack.append('10')
        self.rpn.clear_stack()
        self.assertEqual(self.rpn.stack, [])

    def test_is_num(self):
        self.assertEqual(self.rpn.is_num('5.0'), True)
        self.assertEqual(self.rpn.is_num('.3'), True)
        self.assertEqual(self.rpn.is_num('11.8'), True)
        self.assertEqual(self.rpn.is_num('a'), False)
        self.assertEqual(self.rpn.is_num('sin'), False)

    def test_unary_minus(self):
        self.assertEqual(self.rpn.unary_minus(5), -5)
        self.assertEqual(self.rpn.unary_minus(-5.6), 5.6)
        self.assertEqual(self.rpn.unary_minus(-.8), 0.8)

    def test_unary_plus(self):
        self.assertEqual(self.rpn.unary_plus(6), 6)
        self.assertEqual(self.rpn.unary_plus(-88.6), -88.6)
        self.assertEqual(self.rpn.unary_plus(.1), 0.1)

    def test_factorial(self):
        self.assertEqual(self.rpn.factorial(10), math.factorial(10))
        with self.assertRaises(ValueError):
            self.rpn.factorial(-13)
        with self.assertRaises(ValueError):
            self.rpn.factorial(666.6)

    def test_logarithm(self):
        self.assertEqual(self.rpn.logarithm(8, 2), math.log(8, 2))
        with self.assertRaises(ZeroDivisionError):
            self.rpn.logarithm(8, 1)
        with self.assertRaises(ValueError):
            self.rpn.logarithm(-8, -2)

    def test_logarithm_e(self):
        self.assertEqual(self.rpn.logarithm_e(13), math.log(13))
        with self.assertRaises(ValueError):
            self.rpn.logarithm_e(-20)

    def test_resolve_log(self):
        self.rpn.tokens = ['log', '(', '8', ',', '2', ')']
        self.rpn.resolve_log()
        self.assertEqual(self.rpn.tokens[0], 'log')
        self.rpn.tokens = ['log', '(', '8', ')']
        self.rpn.resolve_log()
        self.assertEqual(self.rpn.tokens[0], 'ln')

    def test_logarithm_two(self):
        self.assertEqual(self.rpn.logarithm_two(8), math.log2(8))
        with self.assertRaises(ValueError):
            self.rpn.logarithm_two(-666)

    def test_logarithm_ten(self):
        self.assertEqual(self.rpn.logarithm_ten(8), math.log10(8))
        with self.assertRaises(ValueError):
            self.rpn.logarithm_ten(-666)

    def test_power(self):
        self.assertEqual(self.rpn.power(2, 4), math.pow(2, 4))
        self.assertEqual(self.rpn.power(10, 2), math.pow(10, 2))
        self.assertEqual(self.rpn.power(3, -2), math.pow(3, -2))
        with self.assertRaises(ValueError):
            self.rpn.power(-2, 1.5)

    def test_square_root(self):
        self.assertEqual(self.rpn.square_root(16), math.sqrt(16))
        self.assertEqual(self.rpn.square_root(101.1), math.sqrt(101.1))
        with self.assertRaises(ValueError):
            self.rpn.square_root(-2)

    def test_divide(self):
        self.assertEqual(self.rpn.divide(18, -2.5), 18 / -2.5)
        with self.assertRaises(ZeroDivisionError):
            self.rpn.divide(-2, 0)

    def test_int_divide(self):
        self.assertEqual(self.rpn.int_divide(1813, 22), 1813 // 22)
        with self.assertRaises(ZeroDivisionError):
            self.rpn.int_divide(-2, 0)

    def test_division_rest(self):
        self.assertEqual(self.rpn.division_rest(131, 0.8), 131 % 0.8)
        with self.assertRaises(ZeroDivisionError):
            self.rpn.division_rest(13, 0)

    def test_add_implicit_multiply(self):
        token_list1 = ['2', '(', '10', '+', '1'')']
        token_list2 = ['8', 'sin', '(', '10', '+', '1'')']
        token_list3 = ['(', '3', ')', '(', '10', '+', '1', ')']
        token_list4 = ['e', 'pi']
        self.assertEqual(self.rpn.add_implicit_multiply(token_list1), ['2', '*', '(', '10', '+', '1'')'])
        self.assertEqual(self.rpn.add_implicit_multiply(token_list2), ['8', '*', 'sin', '(', '10', '+', '1'')'])
        self.assertEqual(self.rpn.add_implicit_multiply(token_list3), ['(', '3', ')', '*', '(', '10', '+', '1', ')'])
        self.assertEqual(self.rpn.add_implicit_multiply(token_list4), ['e', '*', 'pi'])

    def test_resolve_unary(self):
        token_list1 = ['+', '13']
        token_list2 = ['-', 'sin', '(', 'pi', ')']
        self.assertEqual(self.rpn.resolve_unary(token_list1), ['plus', '13'])
        self.assertEqual(self.rpn.resolve_unary(token_list2), ['minus', 'sin', '(', 'pi', ')'])

    def test_resolve_double_const(self):
        self.assertEqual(self.rpn.resolve_double_const('epi + pitau'), 'e pi + pi tau')

    def test_create_tokens_list(self):
        result1 = ['3', '+', '2', '-', 'log', '(', '8', ',', '2', ')']
        self.assertEqual(self.rpn.create_tokens_list('3+2-log(8,2)'), result1)
        result2 = ['sin', '(', 'pi', '/', '2', ')']
        self.assertEqual(self.rpn.create_tokens_list('sin(pi/2)'), result2)

    def test_convert_to_rpn(self):
        expression = '-sin(pi/2)'
        self.assertEqual(self.rpn.convert_to_rpn(expression), ['pi', '2', '/', 'sin', 'minus'])
        expression = 'sen(pi/2)'
        with self.assertRaises(pycalc.UnknownFunctionError):
            self.rpn.convert_to_rpn(expression)

    def test_pop_one(self):
        self.rpn.stack = [1, 2, 3, 4]
        self.assertEqual(self.rpn.pop_one(), 4)

    def test_pop_two(self):
        self.rpn.stack = [1, 2, 3, 4]
        self.assertEqual(self.rpn.pop_one(), 4, 3)

    def test_handle_operations(self):
        rpn_expression1 = ['pi', '2', '/', 'sin', 'minus']
        self.assertEqual(self.rpn.handle_operations(rpn_expression1), -1)
