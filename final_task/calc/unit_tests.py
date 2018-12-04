import unittest

from calc.other_functions import *
from calc.main_functions import *


class TestFindingElements(unittest.TestCase):
    """Test for function 'finding_elements' from other_functions.py"""

    def test1_fe1(self):
        formated_expression = finding_elements('3 >= 5')
        self.assertEqual(formated_expression, [3, ' ', '>', '=', ' ', 5, ' '])

    def test2_fe2(self):
        formated_expression = finding_elements('3.234')
        self.assertEqual(formated_expression, [3.234, ' '])

    def test3_fe3(self):
        formated_expression = finding_elements('epi')
        self.assertEqual(formated_expression, [2.718281828459045, 3.141592653589793, ' '])

    def test4_fe4(self):
        formated_expression = finding_elements('log()')
        self.assertEqual(formated_expression, ['log', '(', ')', ' '])


class TestAdditions(unittest.TestCase):
    """Test for function 'additions' from other_functions.py"""

    def test5_ad1(self):
        formated_expression = additions([3, ' ', '>', '=', ' ', 5, ' '])
        self.assertEqual(formated_expression, [3, '>=', 5])

    def test6_ad2(self):
        formated_expression = additions([3.234, ' '])
        self.assertEqual(formated_expression, [3.234])

    def test7_ad3(self):
        formated_expression = additions([2.718281828459045, 3.141592653589793, ' '])
        self.assertEqual(formated_expression, [2.718281828459045, '*', 3.141592653589793])

    def test8_ad4(self):
        formated_expression = additions(['log', '(', ')', ' '])
        self.assertEqual(formated_expression, ['log', '(', ')'])

    def test9_ad5(self):
        formated_expression = additions(['log', 10, '(', ')', ' '])
        self.assertEqual(formated_expression, ['log10', '(', ')'])

    def test10_ad6(self):
        formated_expression = additions([' ', '-', '+', '-', '-'])
        self.assertEqual(formated_expression, ['-'])


class TestGetLineArgs(unittest.TestCase):
    """Test for function 'get_line_args' from other_functions.py"""

    def test11_gl1(self):
        formated_expression = get_line_args(6, [0, 1, 2, 3, 4, 5, 'log', '(', 2, '*', '(', ')', 4, ')', ')', '(', ')'])
        self.assertEqual(formated_expression, ['(', 2, '*', '(', ')', 4, ')'])


class TestGetArgs(unittest.TestCase):
    """Test for function 'get_args' from other_functions.py"""

    def test12_ga1(self):
        formated_expression = get_args(['(', 2, '*', '(', ')', 4, ')'])
        self.assertEqual(formated_expression, [[2, '*', '(', ')', 4]])

    def test13_ga2(self):
        """Few arguments"""

        formated_expression = get_args(['(', '(', 2, ')', ',', 4, ',', '(', ')', ')'])
        self.assertEqual(formated_expression, [['(', 2, ')'], [4], ['(', ')']])

    def test14_ga3(self):
        """Function in function"""

        formated_expression = get_args(['(', 'log', '(', 2, ',', 2, ')', ',', 4, ')'])
        self.assertEqual(formated_expression, [['log', '(', 2, ',', 2, ')'], [4]])




unittest.main()
