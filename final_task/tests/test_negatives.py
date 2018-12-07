from unittest import TestCase

from libs.element import Element, NoExpressionException, BracketsAreNotBalanced, \
    DoubleOperationException, ExpressionFormatException, UnsupportedMathematicalOperationException, \
    UnsupportedMathematicalFunctionException


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

    def test_comparison_format_exception(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="2*4>")
            expression.value()

    def test_unsupported_comparison_operation(self):
        with self.assertRaises(UnsupportedMathematicalOperationException):
            expression = Element(expression="10<<=4*3")
            expression.value()

    def test_unsupported_operation(self):
        with self.assertRaises(DoubleOperationException):
            expression = Element(expression="1+/5*3")
            expression.value()

    def test_unsupported_trigonometric_operation(self):
        with self.assertRaises(UnsupportedMathematicalFunctionException):
            expression = Element(expression="iii(10)")
            expression.value()

    def test_not_mathematical_constant(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="li")
            expression.value()

    def test_exponentiation(self):
        with self.assertRaises(UnsupportedMathematicalOperationException):
            expression = Element(expression="2**6")
            expression.value()

    def test_expected_arguments(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="pow(2,5,6)")
            expression.value()

    def test_comma_without_func(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="2+3,4")
            expression.value()

    def test_bad_expression(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="--+1-")
            expression.value()

    def test_expression_bad(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="2-")
            expression.value()

    def test_convert_string_to_float(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="21 + 2(3 * 4))")
            expression.value()

    def test_first_comparison(self):
        with self.assertRaises(ExpressionFormatException):
            expression = Element(expression="<=4+6")
            expression.value()

    def test_unsupported_operation(self):
        with self.assertRaises(DoubleOperationException):
            expression = Element(expression="4/*5-3")
            expression.value()
