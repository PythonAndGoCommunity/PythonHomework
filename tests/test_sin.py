import math
from unittest import TestCase

from libs.element import Element


class TestSinElement(TestCase):

    def test_sin(self):
        expression = Element(expression="sin({})".format(math.pi/2))
        self.assertEqual(expression.value(), 1.0)
