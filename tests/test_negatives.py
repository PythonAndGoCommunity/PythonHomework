from unittest import TestCase

from libs.element import Element, NoExpressionException, ExpressionFormatException, BracketsAreNotBalanced, \
    DoubleOperationException, ExpressionFormatException, UnsupportedMathematicalOperationException


class TestNegativesElementSimple(TestCase):

    def test_no_expression(self):
        with self.assertRaises(NoExpressionException):
            expression = Element(expression="")
            expression.value()

    def test_format_expression(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="(5+2)4*5")
            expression.value()

    def test_brackets_are_not_balanced(self):
        with self.assertRaises(BracketsAreNotBalanced):
            expression = Element(expression="((8-3)//5*2")
            expression.value()

    def test_double_operation(self):
        with self.assertRaises(DoubleOperationException):
            expression = Element(expression="(3*2)-/6+2")
            expression.value()

    def test_empty_bracket(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="(2+4)/()")
            expression.value()

    def test_unsupported_operation(self):
        with self.assertRaises(UnsupportedMathematicalOperationException):
            expression = Element(expression="10--4*3")
            expression.value()

    def test_brackets_are_not_balanced_second(self):
        with self.assertRaises(BracketsAreNotBalanced):
            expression = Element(expression="8-3)//5*2")
            expression.value()

    def test_first_negative_value_bad_format(self):
        with self.assertRaises(UnsupportedMathematicalOperationException):
            expression = Element(expression="--2*4-6/2")
            expression.value()
