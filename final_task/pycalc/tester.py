"""Unittests for calculator."""

import unittest
from .validator import Validator
from .calculator import Calculator


class CalculatorTester(unittest.TestCase):
    """Handles all testing operation."""

    def test_calculate(self):
        val = Validator()
        calc = Calculator(val)

        self.assertEqual(calc.calc_start('2'), 2)
        self.assertEqual(calc.calc_start('-2'), -2)

        self.assertEqual(calc.calc_start('2+2'), 4)
        self.assertEqual(calc.calc_start('2-2'), 0)
        self.assertEqual(calc.calc_start('2*2'), 4)
        self.assertEqual(calc.calc_start('2/2'), 1.0)
        self.assertEqual(calc.calc_start('15%2'), 1)
        self.assertEqual(calc.calc_start('2**16'), 65536)

        self.assertEqual(calc.calc_start('2*log10(100)*3'), 12.0)
        self.assertEqual(calc.calc_start('pow(2,2)sqrt(625)'), 100.0)
        self.assertEqual(calc.calc_start('pow(2, 256)'), 2 ** 256)

        self.assertEqual(calc.calc_start('2+2*2'), 6)
        self.assertEqual(calc.calc_start('2/2*2'), 2)
        self.assertEqual(calc.calc_start('2*2/2'), 2)

        self.assertEqual(calc.calc_start('5*(5+5)'), 50)
        self.assertEqual(calc.calc_start('5-(5+5)'), -5)
        self.assertEqual(calc.calc_start('5(5+5)5'), 250)
        self.assertEqual(calc.calc_start('2(2+2)(2+2)2'), 64)
        self.assertEqual(calc.calc_start('2(2((2+2)2))2'), 64)

        self.assertEqual(calc.calc_start(
            '(10-20)(20+10)log10(100)(sqrt(25)+5)'), -6000)
        self.assertEqual(calc.calc_start('32-32*2+50-5**2*2'), -32)
        self.assertEqual(calc.calc_start(
            '9*(2+150*(650/5)-190+445/(20-25))+12+90/5-173036/2*2'), 1.0)
