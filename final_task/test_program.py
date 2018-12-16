import unittest
from program.program import *
from math import *


class ErrorTest(unittest.TestCase):
    """Check Error tests"""

    def test_normal(self):
        result = main_count('2+2')
        self.assertEqual(result, eval('2+2'))

    def test_calc(self):
        result = main_count('2+4')
        self.assertEqual(result, eval('2+4'))

    def test_check_error_null(self):
        result = main_count('')
        self.assertEqual(result, "ERROR: no value")

    def test_check_error_first_sign(self):
        result = main_count('%12')
        self.assertEqual(result, "ERROR: syntax mistake")

    def test_check_error_first_sign2(self):
        result = main_count('\\12')
        self.assertEqual(result, "ERROR: syntax mistake")

    def test_check_error_bad_param(self):
        result = main_count('log(10,2,3)')
        self.assertEqual(result, "ERROR: function arguments are not balanced")

    def test_check_error_not_param(self):
        result = main_count('log()')
        self.assertEqual(result, "ERROR: no function arguments")


class FunctionListTest(unittest.TestCase):
    """Check function work"""

    def test_acos(self):
        result = main_count('acos(1)')
        self.assertEqual(result, eval('acos(1)'))

    def test_acosh(self):
        result = main_count('acosh(1)')
        self.assertEqual(result, eval('acosh(1)'))

    def test_asin(self):
        result = main_count('asin(1)')
        self.assertEqual(result, eval('asin(1)'))

    def test_asinh(self):
        result = main_count('asinh(1)')
        self.assertEqual(result, eval('asinh(1)'))

    def test_atan(self):
        result = main_count('atan(0)')
        self.assertEqual(result, eval('atan(0)'))

    def test_fsum_one_argument(self):
        result = main_count('fsum([9])')
        self.assertEqual(result, eval('fsum([9])'))

    def test_fsum_two_argument(self):
        result = main_count('fsum([9,1])')
        self.assertEqual(result, eval('fsum([9,1])'))

    def test_fsum_more_argument(self):
        result = main_count('fsum([9,1,2,3])')
        self.assertEqual(result, eval('fsum([9,1,2,3])'))

    def test_ceil(self):
        result = main_count('ceil(1)')
        self.assertEqual(result, eval('ceil(1)'))

    def test_degrees(self):
        result = main_count('degrees(1)')
        self.assertEqual(result, eval('degrees(1)'))

    # Check constant
    def test_pi(self):
        result = main_count('pi')
        self.assertEqual(result, eval('pi'))

    def test_e(self):
        result = main_count('e')
        self.assertEqual(result, eval('e'))

    def test_inf(self):
        result = main_count('inf')
        self.assertEqual(result, eval('inf'))

    def test_nan(self):
        result = main_count('nan')
        self.assertEqual(isnan(result), isnan(eval('nan')))

    def test_tau(self):
        result = main_count('tau')
        self.assertEqual(result, eval('tau'))


class CalculateListTest(unittest.TestCase):
    """Check calculating"""

    def test_negative_number(self):
        result = main_count('2+(-3*3-1)')
        self.assertEqual(result, eval('2+(-3*3-1)'))

    def test_del_space(self):
        result = main_count('3*3 -1')
        self.assertEqual(result, eval('3*3 -1'))

    def test_replace_log_1param(self):
        result = main_count('log(2+2)')
        self.assertEqual(result, eval('log(2+2)'))

    def test_replace_log_2param(self):
        result = main_count('log(2,2)')
        self.assertEqual(result, eval('log(2,2)'))

    def test_replace_gcd_2param(self):
        result = main_count('gcd(2,2)')
        self.assertEqual(result, eval('gcd(2,2)'))

    def test_degree_function(self):
        result = main_count('2^sin(2)')
        self.assertEqual(result, eval('2**sin(2)'))

    def test_degree_priority(self):
        result = main_count('2^3^4')
        self.assertEqual(result, eval('2**3**4'))

    def test_degree_negative_number(self):
        result = main_count('2^-3')
        self.assertEqual(result, eval('2**(-3)'))

    def test_negative_numbers(self):
        result = main_count('--+-2')
        self.assertEqual(result, eval('--+-2'))

    def test_negative_numbers_multiplication(self):
        result = main_count('3*-2')
        self.assertEqual(result, eval('3*-2'))

    def test_float_numbers(self):
        result = main_count('3.2-2.875')
        self.assertEqual(result, eval('3.2-2.875'))

    def test_compare_function_more(self):
        result = main_count('3>5')
        self.assertEqual(result, eval('3>5'))

    def test_compare_function_less(self):
        result = main_count('3<=5')
        self.assertEqual(result, eval('3<=5'))

    def test_complex(self):
        result = main_count('3.2+2*cos(e^log(7*e^e^sin(12.3),7.0) + cos(log10(e^-e))+3/2)')
        self.assertEqual(result, eval('3.2+2*cos(e**log(7*e**e**sin(12.3),7.0) + cos(log10(e**-e))+3/2)'))


if __name__ == '__main__':

    unittest.main()
