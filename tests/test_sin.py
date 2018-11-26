import math
from unittest import TestCase

from libs.element import Element


class TestTrigonometricFunctionElement(TestCase):

    def test_sin(self):
        expression = Element(expression="sin({})".format(math.pi / 2))
        self.assertEqual(expression.value(), 1.0)

    def test_cos(self):
        expression = Element(expression="cos({})".format(math.pi * 2))
        self.assertEqual(expression.value(), 1.0)

    def test_tan(self):
        # expression = Element(expression="tan({})".format(math.pi * 3))
        expression = Element(expression="tan(0)")
        self.assertEqual(expression.value(), 0)

    def test_log10(self):
        # expression = Element(expression="cos({})".format(math.pi / 2))
        expression = Element(expression="log10(1)")
        self.assertEqual(expression.value(), 0.0)

    def test_log2(self):
        # expression = Element(expression="cos({})".format(math.pi / 2))
        expression = Element(expression="log2(2)")
        self.assertEqual(expression.value(), 1.0)

    def test_log(self):
        # expression = Element(expression="cos({})".format(math.pi / 2))
        expression = Element(expression="log(1)")
        self.assertEqual(expression.value(), 0.0)

    def test_abs(self):
        # expression = Element(expression="cos({})".format(math.pi / 2))
        expression = Element(expression="abs(10)")
        self.assertEqual(expression.value(), 10.0)
