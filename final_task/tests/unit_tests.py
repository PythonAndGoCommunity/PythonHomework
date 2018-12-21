import unittest
from pycalc.parser import Parser
from pycalc.validator import Validator
from pycalc.importmodules import FunctionParser
from pycalc.operators import operators_dict
from pycalc.evaluator import calculate


class TestLexerMethods(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.function_parser = FunctionParser()
        self.operator = operators_dict['+']
        self.lexem_indicies = [(0, operators_dict['-']), (1, operators_dict['-']), (2, operators_dict['-'])]
        self.lex_arr = [operators_dict['-'],  operators_dict['-'],  operators_dict['-'], '3']

    def test_is_number_method(self):
        self.assertEqual(Parser.is_number('3.03'), True)
        self.assertEqual(Parser.is_number('3.o'), False)
        self.assertEqual(Parser.is_number(self.operator), False)

    def test_is_operator_method(self):
        self.assertEqual(Parser.is_operator('+'), True)
        self.assertEqual(Parser.is_operator('12'), False)

    def test_is_function_method(self):
        self.assertEqual(Parser.is_function('sin'), True)
        self.assertEqual(Parser.is_function('sin1wq'), False)

    def test_is_constant_method(self):
        self.assertEqual(Parser.is_constant('pi'), True)
        self.assertEqual(Parser.is_constant('21'), False)

    def test_find_unary_signs_methods(self):
        self.assertEqual(Parser.find_unary_signs([operators_dict['-'], operators_dict['-'],
                                                 operators_dict['-'], '3']),
                         [(0, operators_dict['-']), (1, operators_dict['-']), (2, operators_dict['-'])])
        self.assertEqual(Parser.find_unary_signs([operators_dict['('], operators_dict['-'], operators_dict['-'],
                                                 operators_dict['-'], '3', operators_dict[')']]),
                         [(1, operators_dict['-']), (2, operators_dict['-']), (3, operators_dict['-'])])

    def test_add_multiply_sign(self):
        self.assertEqual(Parser.add_multiply_sign(['4', self.function_parser.functions_dict['sin']]),
                         ['4', operators_dict['*'], self.function_parser.functions_dict['sin']])
        self.assertEqual(Parser.add_multiply_sign([operators_dict['('], '4', operators_dict[')'],
                                                  self.function_parser.functions_dict['sin']]),
                         [operators_dict['('], '4', operators_dict[')'], operators_dict['*'],
                          self.function_parser.functions_dict['sin']])
        self.assertEqual(Parser.add_multiply_sign([operators_dict['('], '4', operators_dict[')'], operators_dict['('],
                                                  '4', operators_dict[')']]),
                         [operators_dict['('], '4', operators_dict[')'], operators_dict['*'], operators_dict['('], '4',
                          operators_dict[')']])
        self.assertEqual(Parser.add_multiply_sign(['5', operators_dict['('], '4', operators_dict[')']]),
                         ['5', operators_dict['*'], operators_dict['('], '4', operators_dict[')']])

    def test_par_checker(self):
        self.assertFalse(Validator.par_check('(()'))
        self.assertFalse(Validator.par_check('(()))'))
        self.assertFalse(Validator.par_check('(()}'))
        self.assertTrue(Validator.par_check('((((()))))'))
        self.assertTrue(Validator.par_check('3'))
        self.assertTrue(Validator.par_check('((1 + 2))'))

    def test_validation(self):
        expressions = ["2 >= 4 5", "2 > = 45", "3 ! = 4", "2 < = 4", "2 = = 4 5"]
        for expression in expressions:
            with self.assertRaises(ValueError) as context_manager:
                Validator.validate_string(expression)
            self.assertIn("invalid syntax", str(context_manager.exception))
        self.assertEqual(Validator.validate_string("2 >= 45"), "2 >= 45")

    def test_calculate(self):
        exp = 'sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0)))) \
               --cos(1.0)--cos(0.0)^3.0)'
        self.assertEqual(calculate(exp), 0.5361064001012783)
        self.assertEqual(calculate('(3+(4*5)/10)+pow(3,2)'), 14.0)

    def test_parse_expression(self):
        self.assertEqual(self.parser.parse_expression('sin(5)*3'),
                         [self.function_parser.functions_dict['sin'], operators_dict['('], '5', operators_dict[')'],
                          operators_dict['*'], '3'])
