from unittest import TestCase

from libs.element import Element


class TestBracketsElementSimple(TestCase):

    def test_bracket_calculation(self):
        expression = Element(expression="(2+4)/2")
        self.assertEqual(expression.value(), 3)


