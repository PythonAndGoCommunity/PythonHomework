import unittest
import math
from .pycalc import *


class TestLexer(unittest.TestCase):
    def test_skipping_spaces(self):
        self.assertEqual(Lexer('    1       + 2^  3  ').get_all_tokens(), ['1', '+', '2', '^', '3'])

    def test_recognizing_numbers(self):
        self.assertEqual(Lexer('.1').get_all_tokens(), ['.1'])
        self.assertEqual(Lexer('0.001').get_all_tokens(), ['0.001'])
        self.assertEqual(Lexer('000321').get_all_tokens(), ['000321'])
        self.assertEqual(Lexer('1.2345.678').get_all_tokens(), ['1.2345', '.678'])
        self.assertEqual(Lexer('1 2 .3').get_all_tokens(), ['1', '2', '.3'])
        with self.assertRaises(SyntaxError):
            Lexer('.').get_all_tokens()
        with self.assertRaises(SyntaxError):
            Lexer('1..2').get_all_tokens()
        with self.assertRaises(SyntaxError):
            Lexer('1.').get_all_tokens()

    def test_recognizing_parentheses(self):
        self.assertEqual(Lexer('( )(').get_all_tokens(), ['(', ')', '('])

    def test_recognizing_constants(self):
        self.assertEqual(Lexer('epitau').get_all_tokens(), ['e', 'pi', 'tau'])
        self.assertEqual(Lexer('eeepipitau').get_all_tokens(), ['e', 'e', 'e', 'pi', 'pi', 'tau'])

    def test_recognizing_functions(self):
        self.assertEqual(Lexer('pow()abs(round())').get_all_tokens(), ['pow(', ')', 'abs(', 'round(', ')', ')'])
        self.assertEqual(Lexer('log(log10())').get_all_tokens(), ['log(', 'log10(', ')', ')'])
        with self.assertRaises(SyntaxError):
            Lexer('powabs').get_all_tokens()
        with self.assertRaises(SyntaxError):
            Lexer('log100(').get_all_tokens()

    def test_recognizing_operators(self):
        self.assertEqual(Lexer('/*+').get_all_tokens(), ['/', '*', '+'])
        self.assertEqual(Lexer('---+-').get_all_tokens(), ['-', '-', '-', '+', '-'])
        self.assertEqual(Lexer('/////').get_all_tokens(), ['//', '//', '/'])
        self.assertEqual(Lexer('==!===').get_all_tokens(), ['==', '!=', '=='])
        with self.assertRaises(SyntaxError):
            Lexer('= =!=').get_all_tokens()


class TestParser(unittest.TestCase):
    def test_converting_to_rpn(self):
        self.assertEqual(Parser(['-', '5']).convert_to_rpn(), [5.0, '--'])
        self.assertEqual(Parser(['-', '+', '-', '-', '3']).convert_to_rpn(), [3, '--', '--', '++', '--'])
        self.assertEqual(Parser(['1', '^', '2', '^', '3']).convert_to_rpn(), [1, 2, 3, '^', '^'])
        self.assertEqual(Parser(['e', '^', '-', 'e']).convert_to_rpn(), [math.e, math.e, '--', '^'])
        self.assertEqual(Parser(['pi', 'tau']).convert_to_rpn(), [math.pi, math.tau])
        self.assertEqual(Parser(['5', '+', '3', '/', '7']).convert_to_rpn(), [5, 3, 7, '/', '+'])
        self.assertEqual(Parser(['1', '*', '(', '2', '-', '3', ')']).convert_to_rpn(), [1, 2, 3, '-', '*'])
        self.assertEqual(Parser(['pow(', '3', ',', '2', ')', '+', '7']).convert_to_rpn(),
            [[3, ',', 2], 'pow', 7, '+'])
        self.assertEqual(Parser(['pow(', '1', '*', '2', ',', '2', ')']).convert_to_rpn(),
            [[1, 2, '*', ',', 2], 'pow'])
        self.assertEqual(Parser(['abs(', 'abs(', '-', '3', ')', ')']).convert_to_rpn(),
            [[[3, '--'], 'abs'], 'abs'])
        self.assertEqual(Parser(['abs(', '(', '(', '(', '5', ')', ')', ')', ')']).convert_to_rpn(),
            [[5], 'abs'])
        self.assertEqual(Parser(['1', '==', '1', '==', '1', '*', '1']).convert_to_rpn(),
            [1, 1, '==', 1, 1, '*', '=='])
        self.assertEqual(Parser(['sin(', 'pi', '/', '2', ')', '^', '3']).convert_to_rpn(),
            [[math.pi, 2, '/'], 'sin', 3, '^'])
        with self.assertRaises(SyntaxError):
            Parser(['(']).convert_to_rpn()
        with self.assertRaises(SyntaxError):
            Parser(['(', ')', ')']).convert_to_rpn()
        with self.assertRaises(SyntaxError):
            Parser(['1', '*', '*', '2']).convert_to_rpn()
        with self.assertRaises(SyntaxError):
            Parser(['pow(', '5', '*', '(', '3', ',', '4', ')', '+', '3', ')']).convert_to_rpn()


class TestCalculator(unittest.TestCase):
    def test_calculating(self):
        self.assertEqual(calculate([[1, ',', 2, ',', 3, ',', 4, ',', 5], 'fsum']), [15])
        self.assertEqual(calculate([[3, '--'], 'abs']), [3])
        with self.assertRaises(SyntaxError):
            calculate([[1, ',', 2, ',', 3], 'pow'])
        with self.assertRaises(SyntaxError):
            calculate([[1, ',', 2], 'abs'])
        with self.assertRaises(SyntaxError):
            calculate([[','], 'pow'])
        with self.assertRaises(SyntaxError):
            calculate([[3, ','], 'pow'])
        with self.assertRaises(SyntaxError):
            calculate([[], 'abs'])
        with self.assertRaises(SyntaxError):
            calculate([])
        with self.assertRaises(SyntaxError):
            calculate(['--', '--'])
        with self.assertRaises(SyntaxError):
            calculate([1, '-'])
        with self.assertRaises(SyntaxError):
            calculate([1, 2])
        with self.assertRaises(SyntaxError):
            calculate([1, 2, '>', '=='])


if __name__ == '__main__':
    unittest.main()
