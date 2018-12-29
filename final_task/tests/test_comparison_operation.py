
from unittest import TestCase

from libs.element import Element


class TestComparisonFunctionElement(TestCase):

    def test_more_or_equal(self):
        expression = Element(expression="3+14>=2-1")
        self.assertEqual(expression.value(), True)

    def test_less_or_equal(self):
        expression = Element(expression="2-1<=5+4")
        self.assertEqual(expression.value(), True)

    def test_less(self):
        expression = Element(expression="2<4")
        self.assertEqual(expression.value(), True)

    def test_equal(self):
        expression = Element(expression="9==5+4")
        self.assertEqual(expression.value(), True)

    def test_more(self):
        expression = Element(expression="10>5+4")
        self.assertEqual(expression.value(), True)

    def test_not_equal(self):
        expression = Element(expression="1!=5")
        self.assertEqual(expression.value(), True)

    def test_negative_more_or_equal(self):
        expression = Element(expression="3+14>=20-1")
        self.assertEqual(expression.value(), False)

    def test_negative_less_or_equal(self):
        expression = Element(expression="12-1<=5+4")
        self.assertEqual(expression.value(), False)

    def test_negative_less(self):
        expression = Element(expression="8<4")
        self.assertEqual(expression.value(), False)

    def test_negative_equal(self):
        expression = Element(expression="9==5-4")
        self.assertEqual(expression.value(), False)

    def test_negative_more(self):
        expression = Element(expression="10>5+14")
        self.assertEqual(expression.value(), False)

    def test_negative_not_equal(self):
        expression = Element(expression="15<>15")
        self.assertEqual(expression.value(), False)
