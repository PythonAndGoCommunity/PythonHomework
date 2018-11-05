"""This module contains unit tests for methods from all pycalc modules"""

# general import
import unittest

# import of classes to be tested from pycalc modules
from .tokenizer import Tokenizer
from .addmultsigns import Multsignsadder
from .rpn import RPN
from .constsreplacer import Constsreplacer
from .rpncalculator import RPNcalculator


# Tests of 'Tokenizer' class from 'tokenizer' module
class TokenizerTestCase(unittest.TestCase):
    """Tests for Tokenizer class"""
        
    def test_extract_operators_and_pos_int_numbers(self):
        """Are operators and positive int numbers extracted properly?"""
        user_expr = '1+2-3*4/5^6**7//8%9'
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['1', '+', '2', '-', '3', '*', '4', '/',
                                  '5', '^', '6', '**', '7', '//', '8', '%', '9'])
        self.assertEqual(error_msg, None)
        
    def test_extract_operators_and_neg_int_numbers(self):
        """Are operators and negative int numbers extracted properly?"""
        user_expr = '-1+-2--3*-4/-5^-6**-7//-8%-9'
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['-1.0', '-', '2', '+', '3', '*', '-4', '/', '-5',
                                  '^', '-6', '**', '-7', '//', '-8', '%', '-9'])
        self.assertEqual(error_msg, None)
        
    def test_extract_pos_float_numbers(self):
        """Are positive float numbers extracted properly?"""
        user_expr = '0.1+1.55-112.12'
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['0.1', '+', '1.55', '-', '112.12'])
        self.assertEqual(error_msg, None)
        
    def test_extract_neg_float_numbers(self):
        """Are negative float numbers extracted properly?"""
        user_expr = '-0.1+-1.55--112.12'
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['-0.1', '-', '1.55', '+', '112.12'])
        self.assertEqual(error_msg, None)
        
    def test_extract_comparison_operators(self):
        """Are comparison operators extracted properly?"""
        user_expr = '><>=<=!==='
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['>', '<', '>=', '<=', '!=', '=='])
        self.assertEqual(error_msg, None)
        
    def test_extract_pos_constants(self):
        """Are positive constants extracted properly?"""
        user_expr = 'e+pi-tau/inf*nan'
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['e', '+', 'pi', '-', 'tau', '/', 'inf', '*', 'nan'])
        self.assertEqual(error_msg, None)
        
    def test_extract_neg_constants(self):
        """Are negative constants extracted properly?"""
        user_expr = '-e+-pi--tau/-inf*-nan'
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['-e', '-', 'pi', '+', 'tau', '/', '-inf', '*', '-nan'])
        self.assertEqual(error_msg, None)
        
    def test_extract_brackets(self):
        """Are brackets extracted properly?"""
        user_expr = '()'
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['(', ')'])
        self.assertEqual(error_msg, None)
        
    def test_extract_comma(self):
        """Is comma extracted?"""
        user_expr = 'pow(2,3)'
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['pow', '(', '2', ',', '3', ')'])
        self.assertEqual(error_msg, None)
        
    def test_extract_functions(self):
        """Are functions extracted properly?"""
        user_expr = "round(sin(2)-asin(1))-abs(exp(3))"
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['round', '(', 'sin', '(', '2', ')', '-', 'asin', '(', '1', ')', ')',
                                  '-', 'abs', '(', 'exp', '(', '3', ')', ')'])
        self.assertEqual(error_msg, None)

    def test_consider_sub_signs_method(self):
        """Are several subtraction and addition signs replaced by one integrated sign?"""
        user_expr = '-1---2+-3+++4+-2'
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(tokens, ['-1.0', '-', '2', '-', '3', '+', '4', '-', '2'])
        self.assertEqual(error_msg, None)

    def test_is_number_method(self):
        """Does 'is_number' method distinguish tokens which are numbers from ones which are not?"""
        tokens = ['.3', '-0.3', '7', 'tan']
        tokenizer = Tokenizer(user_expr='')
        is_numbers = []
        for token in tokens:
            is_numbers.append(tokenizer.is_number(token))
        self.assertEqual(is_numbers, [True, True, True, False])
        
    def test_extract_tokens_error_msg(self):
        """Is error_message created?"""
        user_expr = "2+shikaka(3)"
        tokenizer = Tokenizer(user_expr)
        tokens, error_msg = tokenizer.extract_tokens()
        self.assertEqual(error_msg, 'ERROR: invalid syntax')


# Tests of 'Multsignsadder' class from 'addmultsigns' module
class MultsignsadderTestCase(unittest.TestCase):
    """Tests for Multsignsadder class"""
        
    def test_is_number_method(self):
        """Does 'is_number' method distinguish tokens which are numbers from ones which are not?"""
        tokens = ['2.3', '-0.6', '5', 'sin', 'exp']
        mult_signs_adder = Multsignsadder(tokens)
        is_numbers = []
        for token in tokens:
            is_numbers.append(mult_signs_adder.is_number(token))
        self.assertEqual(is_numbers, [True, True, True, False, False])
        
    def test_addmultsigns_add_mult_signs(self):
        """Are multiplication signs added to where they implicit were to be in expression?"""
        tokens = ['5', 'tau', '-', '4', 'sin', '(', '7', ')', '-', '9', '(', '1', '+', '10', ')']
        mult_signs_adder = Multsignsadder(tokens)
        extd_tokens = mult_signs_adder.addmultsigns()
        self.assertEqual(extd_tokens, ['5', '*', 'tau', '-', '4', '*', 'sin', '(', '7', ')', '-',
                                       '9', '*', '(', '1', '+', '10', ')'])
        
    def test_addmultsigns_dont_add_mult_signs(self):
        """Aren't multiplication signs added if it's not needed?"""
        tokens = ['2', '+', '3', '*', '5']
        mult_signs_adder = Multsignsadder(tokens)
        extd_tokens = mult_signs_adder.addmultsigns()
        self.assertEqual(extd_tokens, ['2', '+', '3', '*', '5'])

    def test_consider_neg_funcs_method(self):
        """Are negative functions tokens replaced by '-1*function' tokens?"""
        tokens = ['2', '*', '-sin', '(', '2', ')']
        mult_signs_adder = Multsignsadder(tokens)
        mult_signs_adder.consider_neg_functions(mult_signs_adder.tokens)
        self.assertEqual(mult_signs_adder.tokens, ['2', '*', '-1', '*', 'sin', '(', '2', ')'])

    def test_consider_log_args_method(self):
        """Is 'e' added as a base for log functions if last was entered with one argument?"""
        tokens = ['log', '(', '33', ')']
        mult_signs_adder = Multsignsadder(tokens)
        mult_signs_adder.consider_log_args(mult_signs_adder.tokens)
        self.assertEqual(mult_signs_adder.tokens, ['log', '(', '33', ',', 'e', ')'])


# Tests of 'RPN class' from 'rpn' module
class RPNTestCase(unittest.TestCase):
    """Tests for RPN class"""
    
    def test_is_left_associative_method(self):
        """Are left associative operators recognized?"""
        tokens = ['^', '**', '+', '/']
        rpn = RPN(tokens)
        is_left_associative = []
        for token in tokens:
            is_left_associative.append(rpn.is_left_associative(token))
        self.assertEqual(is_left_associative, [False, False, True, True])
        
    def test_is_number_method(self):
        """Does 'is_number' method distinguish tokens which are numbers from ones which are not?"""
        tokens = ['1.3', '-0.5', '/', '%', '9']
        rpn = RPN(tokens)
        is_numbers = []
        for token in tokens:
            is_numbers.append(rpn.is_number(token))
        self.assertEqual(is_numbers, [True, True, False, False, True])
        
    def test_convert2rpn_method(self):
        """Does 'convert2rpn' method work correctly?"""
        tokens = ['-pi', '*', 'round', '(', '2.23', ')', '//', '5', '*', 'pow', '(', '2', '3', ')']
        rpn = RPN(tokens)
        result, error_msg = rpn.convert2rpn()
        self.assertEqual(result, ['-pi', '2.23', 'round', '*', '5', '//', '2', '3', 'pow', '*'])
        self.assertEqual(error_msg, None)
        
    def test_convert2rpn_method_error_msg(self):
        """Is error_message created?"""
        tokens = ['(', '2', '+', '3', ')', ')']
        rpn = RPN(tokens)
        result, error_msg = rpn.convert2rpn()
        self.assertEqual(error_msg, 'ERROR: brackets are not balanced')


# Tests of 'Constsreplacer' class from 'constsreplacer' module
class ConstsreplacerTestCase(unittest.TestCase):
    """Tests for Constsreplacer class"""
    
    def test_replace_constants_method(self):
        """Are constants replaced and not constants aren't replaced?"""
        tokens = ['e', '-e', 'pi', '-pi', 'tau', '-tau', '2', 'cos', 'inf', '-nan', '+']
        constsreplacer = Constsreplacer(tokens)
        replaced_tokens = constsreplacer.replace_constants()
        self.assertEqual(replaced_tokens, ['2.718281828459045', '-2.718281828459045',
                                           '3.141592653589793', '-3.141592653589793',
                                           '6.283185307179586', '-6.283185307179586',
                                           '2', 'cos', 'inf', '-nan', '+'])


# Tests of 'RPNcalculator' class from 'rpncalculator' module
class RPNcalculatorTestCase(unittest.TestCase):
    """Tests for RPNcalculator class"""
    
    def test_evaluate_method_result(self):
        """Does 'evaluate' method actually evaluate RPN math expression and give out correct result?"""
        rpn_tokens = ['2', 'sqrt', '3', '/', '3.14', '*', 'tan']
        rpncalculator = RPNcalculator(rpn_tokens)
        result, error_msg = rpncalculator.evaluate()
        self.assertEqual(result, 11.009005500434151)
        self.assertEqual(error_msg, None)
        
    def test_evaluate_method_error_msg_zero_division(self):
        """Is 'division by zero' error message created?"""
        rpn_tokens = ['2', '0', '/']
        rpncalculator = RPNcalculator(rpn_tokens)
        result, error_msg = rpncalculator.evaluate()
        self.assertEqual(error_msg, 'ERROR: float division by zero')
        
    def test_evaluate_method_error_msg_neg_num_in_fract_pow(self):
        """Is 'negative number cannot be raised to a fractional power' error message created?"""
        rpn_tokens = [['-2', '0.5', '**'], ['-2', '0.5', '^']]
        error_msgs = []
        for rpn_tokens_list in rpn_tokens:
            rpncalculator = RPNcalculator(rpn_tokens_list)
            error_msgs.append(rpncalculator.evaluate()[1])
        for error_msg in error_msgs:
            self.assertEqual(error_msg, 'ERROR: negative number cannot be raised to a fractional power')
            
    def test_evaluate_method_error_msg_neg_num_sqrt(self):
        """Is 'root can't be extracted from a negative number' error message created?"""
        rpn_tokens = ['-2', 'sqrt']
        rpncalculator = RPNcalculator(rpn_tokens)
        result, error_msg = rpncalculator.evaluate()
        self.assertEqual(error_msg, "ERROR: a root can't be extracted from a negative number")
        
    def test_evaluate_method_error_msg_invalid_syntax(self):
        """Is 'invalid syntax' error message created?"""
        rpn_tokens = ['2', '+']
        rpncalculator = RPNcalculator(rpn_tokens)
        result, error_msg = rpncalculator.evaluate()
        self.assertEqual(error_msg, "ERROR: invalid syntax")
        

if __name__ == '__main__':
    unittest.main()
