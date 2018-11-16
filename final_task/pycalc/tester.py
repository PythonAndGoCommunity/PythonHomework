"""Unittests for calculator."""

import math
import unittest
from .validator import Validator
from .calculator import Calculator


class ValidatorTester(unittest.TestCase):
    """Handles all validator testing operations."""

    val = Validator()

    def test_validate(self):
        """Tests most common cases in validator."""

        with self.assertRaises(SystemExit):
            self.val.validate('((')

        with self.assertRaises(SystemExit):
            self.val.validate('')

        with self.assertRaises(SystemExit):
            self.val.validate('1 2 3 4 5 + 6')

        with self.assertRaises(SystemExit):
            self.val.validate('123 >      = 5')

    def test_check(self):
        """Tests fast checking function."""

        with self.assertRaises(SystemExit):
            self.val.check('*', None, 1)

        with self.assertRaises(SystemExit):
            self.val.check('^', -1, 1.5)


class CalculatorTester(unittest.TestCase):
    """Handles all calculator testing operations."""

    val = Validator()
    calc = Calculator(val)

    def test_calc_start(self):
        """Checks most common calculating cases."""

        tests = (
            ('2', 2),
            ('-2', -2),
            ('2', 2),
            ('-2', -2),
            ('2+2', 2+2),
            ('2-2', 2-2),
            ('2*2', 2*2),
            ('2/2', 2/2),
            ('15%2', 15 % 2),
            ('2**16', 2**16),
            ('2*log10(100)*3', 12.0),
            ('pow(2,2)sqrt(625)', 100.0),
            ('pow(2, 256)', 2 ** 256),
            ('eexp(e)', 41.193555674716116),
            ('2+2*2', 2+2*2),
            ('2/2*2', 2/2*2),
            ('2*2/2', 2*2/2),
            ('5*(5+5)', 5*(5+5)),
            ('5-(5+5)', 5-(5+5)),
            ('5(5+5)5', 5*(5+5)*5),
            ('2(2+2)(2+2)2', 2*(2+2)*(2+2)*2),
            ('2(2((2+2)2))2', 2*(2*((2+2)*2))*2),
            ('(10-20)(20+10)log10(100)(sqrt(25)+5)', -6000),
            ('32-32*2+50-5**2*2', 32-32*2+50-5**2*2),
            ('9*(2+150*(650/5)-190+445/(20-25))+12+90/5-173036/2*2', 1.0)
        )

        for test, result in tests:
            self.assertEqual(self.calc.calc_start(test), result)

    def test_find_left_num(self):
        """Tests if left number is found correctly."""

        result = self.calc.find_left_num('-125.125+10', 8)
        self.assertEqual(result, '-125.125')

    def test_find_right_num(self):
        """Tests if right number is found correctly."""

        result = self.calc.find_right_num('-125.125+10', 8)
        self.assertEqual(result, '10')

    def test_find_sign_pos(self):
        """Tests if sign position is found correctly."""

        result = self.calc.find_sign_pos('12345678^87654321', '^')
        self.assertEqual(result, 8)

    def test_calculate_functions(self):
        """Tests function calculating method."""

        result = self.calc.calculate_functions('log10(100)*2')
        self.assertEqual(result, '[2.0]*2')

    def test_get_func_args(self):
        """Tests arguments fonding method."""

        result = self.calc.get_func_args(
            '2*2*2*any_func(5,(6+7),((8+9)+10))', 'any_func', 6
        )
        self.assertEqual(result, (['5', '(6+7)', '((8+9)+10)'], 34))

    def test_replace_constants(self):
        """Tests if constants are replaced correctly."""

        result = self.calc.replace_constants('2pietau')
        self.assertEqual(
            result,
            '2(3.141592653589793)(2.718281828459045)(6.283185307179586)'
        )

    def test_get_reserved_by_name(self):
        """Tests if function object is got properly by its name."""

        result = self.calc.get_reserved_by_name('log')
        self.assertEqual(result, math.log)

    def test_convert(self):
        """Tests correctness of string to number/boolean conversion."""

        self.assertEqual(self.calc.convert('2'), 2)
        self.assertEqual(self.calc.convert('.1'), 0.1)
        self.assertEqual(self.calc.convert('True'), True)

    def test_convert_arguments(self):
        """Tests function arguments conversion."""

        result = self.calc.convert_arguments(['2', 'log10(100)', '(2+2)'])
        self.assertEqual(result, [2, 2.0, 4])

    def test_handle_subtraction(self):
        """Tests correctness of subtraction replacing."""

        result = self.calc.handle_subtraction('2-1000*2(-100-50)')
        self.assertEqual(result, '2+-1000*2(-100+-50)')

    def test_handle_implicit_multiplication(self):
        """Tests correctness of implicit multiplication replacing."""

        result = self.calc.handle_implicit_multiplication('2(10)(10)5')
        self.assertEqual(result, '2*(10)*(10)*5')

    def test_handle_extra_signs(self):
        """Tests correctness of getting rid of extra signs."""

        result = self.calc.handle_extra_signs('1----1+++++++1-+-+-+-+---+2')
        self.assertEqual(result, '1+1+1+-2')

    def test_calculate_elementary(self):
        """Tests elementary binary operations calculating."""

        result = self.calc.calculate_elementary('*', '1', '2')
        self.assertEqual(result, 2)

    def test_calculate_nested(self):
        """Checks correctness of calculating nested expressions."""

        result = self.calc.calculate_nested('((2*(((10+10)))))')
        self.assertEqual(result, '[40]')

    def test_get_nested(self):
        """Checks correctness of getting nested with no nested inside it."""

        result = self.calc.get_nested('(10*10(10*10)(10*10(20*20)))')
        self.assertEqual(result, '(10*10)')
