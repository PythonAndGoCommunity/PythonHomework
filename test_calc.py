import unittest, calc


class TestCalc(unittest.TestCase):

    def test_correct_expression(self):
        expect = ['-1', '*', 'sin', '(', '30', ')', '+', '0.25', '-', '(', '-1', '*', 'pow', '(', '2', ',', '2', ')',
                  ')']
        actual = calc.correct_expression('-sin(30)+.25-(-pow(2, 2))')
        self.assertEqual(expect, actual)

    def test_insert_multiplication(self):
        expect = '3*log10(2)*5+2*(2+3)*(7+1)*log1p(8)'
        actual = calc.insert_multiplication('3log10(2)5+2(2+3)(7+1)log1p(8)')
        self.assertEqual(expect, actual)

    def test_correct_negative_value(self):
        expect = '-1sin(40+5)+3(-1pi)'
        actual = calc.match_negative_value('-sin(40+5)+3(-pi)')
        self.assertEqual(expect, actual)

    def test_zeroless_number(self):
        expect = '5+0.25*0.3abs(-0.75)'
        actual = calc.zeroless('5+.25*.3abs(-.75)')
        self.assertEqual(expect, actual)
