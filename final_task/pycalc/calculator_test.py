"""Test suite for pycalc.

Unit tests go in "TestCalculator".
"""

import unittest
from math import *

from calculator import Calculator, isnumber

TEST_CASES = {
    "Unary": {
        "-13": -13,
        "6-(-13)": 6-(-13),
        "1---1": 1---1,
        "-+---+-1": -+---+-1},
    "Priority": {
        "1+2*2": 1+2*2,
        "1+(2+3*2)*3": 1+(2+3*2)*3,
        "10*(2+1)": 10*(2+1),
        "10^(2+1)": 10**(2+1),
        "100/3^2": 100/3**2,
        "100/3%2^2": 100/3 % 2**2},
    "Funcs": {
        "pi+e": pi+e,
        "log(e)": log(e),
        "sin(pi/2)": sin(pi/2),
        "log10(100)": log10(100),
        "sin(pi/2)*111*6": sin(pi/2)*111*6,
        "2*sin(pi/2)": 2*sin(pi/2)},
    "Associative": {
        "102%12%7": 102 % 12 % 7,
        "100/4/3": 100/4/3,
        "2^3^4": 2**3**4},
    "Comparison": {
        "1+2*3==1+2*3": eval("1+2*3==1+2*3"),
        "e^5>=e^5+1": eval("e**5>=e**5+1"),
        "1+2*4/3+1!=1+2*4/3+2": eval("1+2*4/3+1!=1+2*4/3+2")
    },
    "Common": {
        "(100)": (100),
        "666": 666,
        "-.1": -.1,
        "1/3": 1/3,
        "1.0/3.0": 1.0/3.0,
        ".1 * 2.0^56.0": .1 * 2.0**56.0,
        "e^34": e**34,
        "(2.0^(pi/pi+e/e+2.0^0.0))": (2.0**(pi/pi+e/e+2.0**0.0)),
        "(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)": (2.0**(pi/pi+e/e+2.0**0.0))**(1.0/3.0),
        "sin(pi/2^1) + log(1*4+2^2+1, 3^2)": sin(pi/2**1) + log(1*4+2**2+1, 3**2),
        "10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5": 10*e**0*log10(.4 - 5 / -0.1-10) - -abs(-53/10) + -5,
        "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+" +
        "cos(sin(sin(34.0-2.0 ^ 2.0))))--cos(1.0)--cos(0.0) ^ 3.0)":
        sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0)))) +
                 cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0),
        "2.0^(2.0^2.0*2.0^2.0)": 2.0**(2.0**2.0*2.0**2.0),
        "sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))":
        sin(e ** log(e ** e ** sin(23.0), 45.0) + cos(3.0 + log10(e ** -e)))
    },
    "Implicit": {
        "2(2+2)": 2*(2 + 2),
        "sin(pi/2)2": sin(pi / 2) * 2,
        "(1+2)(3+4)": (1 + 2)*(3 + 4),
        "cos(pi)log10(100)": cos(pi)*log10(100)
    },
    "Error": [
        "",
        "+",
        "1-",
        "1 2",
        "ee",
        "==7",
        "1 + 2(3 * 4))",
        "((1+2)",
        "1 + 1 2 3 4 5 6 ",
        "log100(100)",
        "------",
        "5 > = 6",
        "5 / / 6",
        "6 < = 6",
        "6 * * 6",
        "((((("]}


class TestCalculator(unittest.TestCase):
    def test_unary(self):
        for t in TEST_CASES['Unary']:
            self.assertEqual(Calculator(t).calc(), TEST_CASES['Unary'][t])

    def test_priority(self):
        for t in TEST_CASES['Priority']:
            self.assertEqual(Calculator(t).calc(), TEST_CASES['Priority'][t])

    def test_funcs(self):
        for t in TEST_CASES['Funcs']:
            self.assertEqual(Calculator(t).calc(), TEST_CASES['Funcs'][t])

    def test_associative(self):
        for t in TEST_CASES['Associative']:
            self.assertEqual(Calculator(t).calc(),
                             TEST_CASES['Associative'][t])

    def test_comparasion(self):
        for t in TEST_CASES['Comparison']:
            self.assertEqual(Calculator(t).calc(), TEST_CASES['Comparison'][t])

    def test_common(self):
        for t in TEST_CASES['Common']:
            self.assertEqual(Calculator(t).calc(), TEST_CASES['Common'][t])

    def test_implicit(self):
        for t in TEST_CASES['Implicit']:
            self.assertEqual(Calculator(t).calc(), TEST_CASES['Implicit'][t])

    def test_errors(self):
        for t in TEST_CASES['Error']:
            with self.assertRaises(Exception):
                Calculator(t).calc()

    def test_isnumber(self):
        self.assertTrue(isnumber('2'))
        self.assertTrue(isnumber('2.2'))
        self.assertFalse(isnumber('2s'))
        self.assertFalse(isnumber('s2'))
        self.assertFalse(isnumber('s2'))


if __name__ == '__main__':
    unittest.main()
