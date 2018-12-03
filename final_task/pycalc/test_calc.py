import unittest
import time
from final_task.pycalc import calc


class TestCalc(unittest.TestCase):

    def test_correct_expression(self):
        expect = ['~', 'sin', '(', '30', ')', '+', '0.25', '-', '(', '~', 'pow', '(', '2', ',', '2', ')',
                  ')']
        actual = calc.correct_expression('-sin(30)+.25-(-pow(2, 2))')
        self.assertEqual(expect, actual)

    def test_insert_multiplication(self):
        expect = '3*log10(2)*5+2*(2+3)*(7+1)*log1p(8)'
        actual = calc.insert_multiplication('3log10(2)5+2(2+3)(7+1)log1p(8)')
        self.assertEqual(expect, actual)

    def test_correct_negative_value(self):
        expect = '~sin(40+5)+3(~pi)'
        actual = calc.match_negative_value('-sin(40+5)+3(-pi)')
        self.assertEqual(expect, actual)

    def test_with_zero_number(self):
        expect = '5+0.25*0.3abs(-0.75)'
        actual = calc.fix_missing_zero('5+.25*.3abs(-.75)')
        self.assertEqual(expect, actual)

    def test_invalid_brackets(self):
        with self.assertRaises(calc.CalcError):
            calc.correct_expression('sin()+3')
            calc.to_postfix('sin30(5-1)')
            calc.to_postfix('(')
            calc.to_postfix('1+2/3+5)-6')

    def test_invalid_input(self):
        with self.assertRaises(calc.CalcError):
            calc.to_postfix('2+3+sin(45)+pov(2, 6)')
            calc.to_postfix('1+2*3-4@')
            calc.to_postfix('1-#/2')
            calc.to_postfix('3*6>>5+7')
            calc.to_postfix('./7+2')
            calc.to_postfix('.7*(sin())')
            calc.to_postfix('23+3+')
            calc.to_postfix('abs(-)')
            calc.correct_expression('')
            calc.correct_expression('-')

    def test_invalid_operators(self):
        with self.assertRaises(calc.CalcError):
            calc.to_postfix('1+2-*6-3')
            calc.to_postfix('cos(*+30)/2+3')

    def test_reversed_polish_notation(self):
        expect = ['3', '5', '2', '2', '^', '*', '3', '1', '-', '/', '+', 'abs', '-2', ')', '-', 'pow', '1', '1', '+',
                  ',', '1', '2', '*', '1', '+', ')', '+']
        actual = calc.to_postfix('3+5*2^2/(3-1)-abs(-2)+pow(1+1, 1*2+1)')
        self.assertEqual(expect, actual)

    def test_comparison(self):
        expect = True
        actual = calc.calc_iteration(calc.to_postfix('2+3*5>=10+12/2'), None)
        self.assertEqual(expect, actual)

    def test_addition(self):
        expect = 8.05
        actual = calc.calc_iteration(calc.to_postfix('3.5+.5+2.75+1.3'), None)
        self.assertEqual(expect, actual)

    def test_subtraction(self):
        expect = 3
        actual = calc.calc_iteration(calc.to_postfix('25-22'), None)
        self.assertEqual(expect, actual)

    def test_multiplication(self):
        expect = 5
        actual = calc.calc_iteration(calc.to_postfix('2.5*2'), None)
        self.assertEqual(expect, actual)

    def test_division(self):
        expect = 6
        actual = calc.calc_iteration(calc.to_postfix('24/4'), None)
        self.assertEqual(expect, actual)

    def test_division_by_zero(self):
        with self.assertRaises(calc.CalcError):
            calc.calc_iteration(calc.to_postfix('3 / 0'), None)

    def test_modulus(self):
        expect = 7
        actual = calc.calc_iteration(calc.to_postfix('29%11'), None)
        self.assertEqual(expect, actual)

    def test_modulo_by_zero(self):
        with self.assertRaises(calc.CalcError):
            calc.calc_iteration(calc.to_postfix('3 % 0'), None)

    def test_floor_division(self):
        expect = 4
        actual = calc.calc_iteration(calc.to_postfix('9//2'), None)
        self.assertEqual(expect, actual)

    def test_floor_division_by_zero(self):
        with self.assertRaises(calc.CalcError):
            calc.calc_iteration(calc.to_postfix('3 // 0'), None)

    def test_power(self):
        expect = 8
        actual = calc.calc_iteration(calc.to_postfix('2^3'), None)
        self.assertEqual(expect, actual)

    def test_round(self):
        expect = 8
        actual = calc.calc_iteration(calc.to_postfix('round(7.51)'), None)
        self.assertEqual(expect, actual)

    def test_abs(self):
        expect = 6
        actual = calc.calc_iteration(calc.to_postfix('abs(-6)'), None)
        self.assertEqual(expect, actual)

    def test_multi_operations(self):
        expect = 2
        actual = calc.evaluate('--1-(+-1)', None)
        self.assertEqual(expect, actual)

    def test_get_args(self):
        expect = ('pow', [['2'], ['3']])
        actual = calc.get_arguments(['pow', '2', ',', '3', ')'])
        self.assertEqual(expect, actual)

    def test_is_function(self):
        expect = (True, True, False, False)
        actual = (calc.is_func('_func_'), calc.is_func('my_func'), calc.is_func('.'), calc.is_func('44'))
        self.assertEqual(expect, actual)

    def test_is_float(self):
        expect = (True, True, False, False)
        actual = (calc.is_float('-2'), calc.is_float('55'), calc.is_float('44,7'), calc.is_float('float'))
        self.assertEqual(expect, actual)

    def test_calc_iteration(self):
        expect = (1, 8)
        actual = (calc.calc_iteration(['sin', 'pi', '2', '/', ')'], None),
                  calc.calc_iteration(['pow', '2', ',', '3', ')'], None))
        self.assertEqual(expect, actual)
