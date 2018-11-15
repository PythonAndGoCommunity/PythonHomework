from unittest import TestCase

from libs.element import Element


class TestElementSimple(TestCase):

    def test_sum(self):
        expression = Element(expression="5+3")
        self.assertEqual(expression.value(), 8)

    def test_div(self):
        expression = Element(expression="5/2")
        self.assertEqual(expression.value(), 2.5)

    def test_double_mod(self):
        expression = Element(expression="9//3//3")
        self.assertEqual(expression.value(), 1)

    def test_math_operator_priority(self):
        expression = Element(expression="5/2+0.1*5")
        self.assertEqual(expression.value(), 3)
