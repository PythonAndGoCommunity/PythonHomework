import unittest, calc


class TestCalc(unittest.TestCase):

    def test_correct_expression(self):
        expect = ['sin', '(', '30', ')', '+', '0.25', '-' , '(', '-1', ')' ]
        actual = calc.correct_expression('sin(30)+.25-(-1)')
        self.assertEqual(actual, expect)

    def test_bad_brackets(self):
        with self.assertRaises(calc.CalcError):
            calc.correct_expression('8-3(5-1))')
