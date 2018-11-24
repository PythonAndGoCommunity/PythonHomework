import unittest

from calc.functions import *
from calc.math_functions import decide_func as d_f

class TestAddingMultiplication(unittest.TestCase):
    """Tests for 'adding_multiply'."""

    def test_multiply1(self):
        """expression '2(2)' formating correctly?"""
        formated_expression = adding_multiply([2.0, '(', 2.0, ')'])
        self.assertEqual(formated_expression, [2.0, '*', '(', 2.0, ')'])

    def test_multiply2(self):
        """expression '2pow(2, 1)' formating correctly?"""
        formated_expression = adding_multiply([2.0, 'pow', '(', 2.0, ',', 1.0, ')'])
        self.assertEqual(formated_expression, [2.0, '*', 'pow', '(', 2.0, ',', 1.0, ')'])

    def test_multiply3(self):
        """expression '(2)2' formating correctly?"""
        formated_expression = adding_multiply(['(', 2.0, ')', 2.0])
        self.assertEqual(formated_expression, ['(', 2.0, ')', '*', 2.0])

    def test_multiply4(self):
        """expression '(2)(2)' formating correctly?"""
        formated_expression = adding_multiply(['(', 2.0, ')', '(', 2.0, ')'])
        self.assertEqual(formated_expression, ['(', 2.0, ')', '*',  '(', 2.0, ')'])

    def test_multiply5(self):
        """expression '(2)pow(2,1)' formating correctly?"""
        formated_expression = adding_multiply(['(', 2.0, ')', 'pow', '(', 2.0, ',', 1.0, ')'])
        self.assertEqual(formated_expression, ['(', 2.0, ')', '*', 'pow', '(', 2.0, ',', 1.0, ')'])

'''
class TestFomatExpression(unittest.TestCase):
    """Tests for finding_elements"""

    def test_format1(self):
        "expression '2(2)pow(2,log1p(-10)) formating correctly?"
        formated_expression = finding_elements(list('(2(2)pow(2,log1p(-10))  '))
        self.assertEqual(formated_expression, ['(', 2.0, '*', '(', 2.0, ')', '*', 'pow',
        '(', 2.0, ',', 'log1p', '(', '-', 10.0, ')', ')', ')'])
'''

class TestSelection(unittest.TestCase):
    """Tests for selection"""

    def test_select1(self):
        "expression 'abs(abs(0))' formating correctly?"
        formated_expession = selection(0, ['abs', '(', 'abs', '(', 0.0, ')', ')'])
        self.assertEqual(formated_expession, ['(', 'abs', '(', 0.0, ')', ')'])

    def test_select2(self):
        "expression 'pow(abs(0), 0)' formating correctly?"
        formated_expession = selection(0, ['pow', '(', 'abs', '(', 0.0, ')', ',', 0.0, ')'])
        self.assertEqual(formated_expession, ['(', 'abs', '(', 0.0, ')', ',', 0.0, ')'])

class TestGettingArgs(unittest.TestCase):
    """Tests for get_args"""

    def test_deciding_args1(self):
        "expression '(abs(0))' formating correctly?"
        formated_expession = get_args(['(', 'abs', '(', 0.0, ')', ')'])
        self.assertEqual(formated_expession, [['(', 'abs', '(', 0.0, ')', ')']])

    def test_deciding_args2(self):
        "expression '(abs(0), 0)' formating correctly?"
        formated_expession = get_args(['(', 'abs', '(', 0.0, ')', ',', 0.0, ')'])
        self.assertEqual(formated_expession, [['(', 'abs', '(', 0.0, ')', ')'], ['(', 0.0, ')']])

class TestDecidingArgs(unittest.TestCase):
    """Tests for deciding_args"""

    def test_get_args1(self):
        "expression '(abs(0), 0)' formating correctly?"
        formated_expession = deciding_args([['(', 'abs', '(', 0.0, ')', ')'], ['(', 0.0, ')']])
        self.assertEqual(formated_expession, [0.0, 0.0])

if __name__ == '__main__':
    unittest.main()
