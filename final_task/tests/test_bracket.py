from unittest import TestCase

from libs.element import Element


class TestBracketsElementSimple(TestCase):

    def test_bracket_calculation(self):
        expression = Element(expression="(2+8)//2+(6-3)")
        self.assertEqual(expression.value(), 8)

    def test_nesting_of_elements_in_brackets(self):
        expression = Element(expression="2+(3*((5-1)-2))")
        self.assertEqual(expression.value(), 8)
