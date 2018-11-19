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

    def test_mul(self):
        expression = Element(expression="5*5-10")
        self.assertEqual(expression.value(), 15)

    def test_double_mul(self):
        expression = Element(expression="5*5*4")
        self.assertEqual(expression.value(), 100)

    def test_modulo(self):
        expression = Element(expression="5%3")
        self.assertEqual(expression.value(), 2)

    def test_first_negative_value(self):
        expression = Element(expression="-2*4-6/2")
        self.assertEqual(expression.value(), -11)

    def test_exponentiation(self):
        expression = Element(expression="2**3//4")
        self.assertEqual(expression.value(), 2)

    def test_nesting_of_elements(self):
        expression = Element(expression="2+(3*((5-1)-2))")
        self.assertEqual(expression.value(), 8)

    def test_str(self):
        expression = Element(expression="2+3*((5-1)-2)")
        self.assertTrue(str(expression), 8)

   
