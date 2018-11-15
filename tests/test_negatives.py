from unittest import TestCase

from libs.element import Element, NoExpressionException


class TestNegativesElementSimple(TestCase):

    def test_no_expression(self):
        with self.assertRaises(NoExpressionException):
            expression = Element(expression="")
            expression.value()
