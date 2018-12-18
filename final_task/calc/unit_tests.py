import unittest
from calc.other_functions import *
from calc.math_functions import decide_func


class TestFindingElements(unittest.TestCase):
    """Test for function 'finding_elements' from other_functions.py"""

    def test_fe1(self):
        formated_expression = finding_elements('3 >= 5')
        self.assertEqual(formated_expression, [3, ' ', '>', '=', ' ', 5, ' '])

    def test_fe2(self):
        formated_expression = finding_elements('3.234')
        self.assertEqual(formated_expression, [3.234, ' '])

    def test_fe3(self):
        formated_expression = finding_elements('epi')
        self.assertEqual(formated_expression, [2.718281828459045, 3.141592653589793, ' '])

    def test_fe4(self):
        formated_expression = finding_elements('log()')
        self.assertEqual(formated_expression, ['log', '(', ')', ' '])


class TestAdditions(unittest.TestCase):
    """Test for function 'additions' from other_functions.py"""

    def test_ad1(self):
        formated_expression = additions([3, ' ', '>', '=', ' ', 5, ' '])
        self.assertEqual(formated_expression, [3, '>=', 5])

    def test_ad2(self):
        formated_expression = additions([3.234, ' '])
        self.assertEqual(formated_expression, [3.234])

    def test_ad3(self):
        formated_expression = additions([2.718281828459045, 3.141592653589793, ' '])
        self.assertEqual(formated_expression, [2.718281828459045, '*', 3.141592653589793])

    def test_ad4(self):
        formated_expression = additions(['log', '(', ')', ' '])
        self.assertEqual(formated_expression, ['log', '(', ')'])

    def test_ad5(self):
        formated_expression = additions(['log', 10, '(', ')', ' '])
        self.assertEqual(formated_expression, ['log10', '(', ')'])

    def test_ad6(self):
        formated_expression = additions([' ', '-', '+', '-', '-'])
        self.assertEqual(formated_expression, ['-'])


class TestGetLineArgs(unittest.TestCase):
    """Test for function 'get_line_args' from other_functions.py"""

    def test_gl1(self):
        formated_expression = get_line_args(6, [0, 1, 2, 3, 4, 5, 'log', '(', 2, '*', '(', ')', 4, ')', ')', '(', ')'])
        self.assertEqual(formated_expression, ['(', 2, '*', '(', ')', 4, ')'])


class TestGetArgs(unittest.TestCase):
    """Test for function 'get_args' from other_functions.py"""

    def test_ga1(self):
        formated_expression = get_args(['(', 2, '*', '(', ')', 4, ')'])
        self.assertEqual(formated_expression, [[2, '*', '(', ')', 4]])

    def test_ga2(self):
        """Few arguments"""

        formated_expression = get_args(['(', '(', 2, ')', ',', 4, ',', '(', ')', ')'])
        self.assertEqual(formated_expression, [['(', 2, ')'], [4], ['(', ')']])

    def test_ga3(self):
        """Function in function"""

        formated_expression = get_args(['(', 'log', '(', 2, ',', 2, ')', ',', 4, ')'])
        self.assertEqual(formated_expression, [['log', '(', 2, ',', 2, ')'], [4]])


class TestMiniFunctions1(unittest.TestCase):
    """Test for minifunction from other_functions.py"""

    def test_vn(self):
        """Function 'verify_num' verify performance"""

        formated_expression = verify_num('12.3456')
        self.assertEqual(formated_expression, 12.3456)

    def test_pe1(self):
        """Function 'verify_pi_e' verify performance"""

        formated_expression = verify_pi_e('pi', [])
        self.assertEqual(formated_expression, '')

    def test_pe2(self):
        """Function 'verify_pi_e' verify performance"""

        formated_expression = verify_pi_e('pow', [])
        self.assertEqual(formated_expression, 'pow')

    def test_pr1(self):
        """Function 'prior' verify performance"""

        formated_expression = get_prior(12.34)
        self.assertEqual(formated_expression, 5)

    def test_pr2(self):
        """Function 'prior' verify performance"""

        formated_expression = get_prior('log')
        self.assertEqual(formated_expression, 5)

    def test_bo(self):
        """Function 'bin_operate' verify performance"""

        formated_expression = perform_bin_operate(2, 2, '^')
        self.assertEqual(formated_expression, 4)


class TestDecideFunction(unittest.TestCase):
    """Test for function 'decide_function' from math_functions.py"""

    def test_mdf(self):
        """verify performance"""

        formated_expression = decide_func('pow', [2, 2])
        self.assertEqual(formated_expression, 4)
