import argparse
import math
import types
from collections import namedtuple

class Lexer:
    """This class extracts tokens from a mathematical expression.
    The expression may contain:
        numbers(e.g. '3', '.15', '12.345');
        parentheses: '(', ')';
        constants: all constants from standard python module 'math';
        operators: '+', '-', '*', '//', '/', '%', '^', '==', '!=', '>=', '>', '<=', '<';
        functions: all functions from standard python module 'math';"""

    PARENTHESES = ('(', ')')
    OPERATORS = ('+', '-', '*', '//', '/', '%', '^', '==', '!=', '>=', '>', '<=', '<')
    CONSTANTS = tuple(key for key, value in math.__dict__.items() if isinstance(value, float))
    FUNCTIONS = tuple(key + '(' for key, value in math.__dict__.items() if isinstance(value, types.BuiltinFunctionType)) \
                   + ('round(', 'abs(')

    def __init__(self, expression):
        self.expression = expression
        self.position = 0
        self.current_token = None
    
    def skip_spaces(self):
        while self.position < len(self.expression) and self.expression[self.position].isspace():
            self.position += 1

    def get_next_token(self):
        """This method returns next token in the expression.
        If the next token can't be recognized, the function raises SyntaxError exception."""

        self.current_token = None
        self.skip_spaces()
       
        if self.position >= len(self.expression):
            return None
        elif self.expression[self.position] == ',':
            self.current_token = ','
            self.position += 1
        elif not (self.recognize_number() or self.recognize_operator() or self.recognize_parenthesis() \
             or self.recognize_function() or self.recognize_constant()):
            raise SyntaxError('ERROR: unrecognized lexeme \'' + self.expression[self.position : ] + '\'.')

        return self.current_token

    def get_all_tokens(self):
        result = []
        while self.get_next_token() != None:
            result.append(self.current_token)
        return result

    def recognize_number(self):
        """This method tries to recognize a number in the expression.
        If the number has found, the function returns True, and False otherwise.
        The number will be placed in self.current_token."""

        was_dot = False
        for index, character in enumerate(self.expression[self.position : ]):
            if not character.isdigit() and (character != '.' or was_dot):
                if index != 0 and self.expression[self.position + index - 1] != '.':
                    self.current_token = self.expression[self.position : self.position + index]
                    self.position += index
                break
            was_dot |= (character == '.')
        else:
            if not self.expression[self.position : ].endswith('.'):
                self.current_token = self.expression[self.position : ]
                self.position = len(self.expression)
        return self.current_token != None

    def recognize_operator(self):
        """This method tries to recognize an operator in the expression.
        If the operator has found, the function returns True, and False otherwise.
        The operator will be placed in self.current_token."""

        for operator in Lexer.OPERATORS:
            if self.expression[self.position : ].startswith(operator):
                self.current_token = operator
                self.position += len(operator)
                break
        return self.current_token != None

    def recognize_constant(self):
        """This method tries to recognize a constant in the expression.
        If the constant has found, the function returns True, and False otherwise.
        The constant will be placed in self.current_token."""

        for constant in Lexer.CONSTANTS:
            if self.expression[self.position : ].startswith(constant):
                self.current_token = constant
                self.position += len(constant)
                break
        return self.current_token != None

    def recognize_function(self):
        """This method tries to recognize a function in the expression.
        If the function has found, the function returns True, and False otherwise.
        The function will be placed in self.current_token."""

        for function in Lexer.FUNCTIONS:
            if self.expression[self.position : ].startswith(function):
                self.current_token = function
                self.position += len(function)
                break
        return self.current_token != None

    def recognize_parenthesis(self):
        """This method tries to recognize parentheses in the expression.
        If the parenthesis have found, the function returns True, and False otherwise.
        The parentheses will be placed in self.current_token."""

        if self.expression[self.position] in Lexer.PARENTHESES:
            self.current_token = self.expression[self.position]
            self.position += 1
        return self.current_token != None

Token = namedtuple('Token', ('priority', 'function', 'args_number'))

class Parser:
    '''This class parses tokens and converts them into reverse polish notation.'''

    TOKENS = {function : Token(5, getattr(math, function), None) for function in dir(math)}
    TOKENS.update({',': Token(0, None, None),
                   '(': Token(0, None, None),
                   ')': Token(0, None, None),
                   '==': Token(1, lambda x, y: x == y, 2),
                   '!=': Token(1, lambda x, y: x != y, 2),
                   '>=': Token(1, lambda x, y: x >= y, 2),
                   '<=': Token(1, lambda x, y: x <= y, 2),
                   '<': Token(1, lambda x, y: x < y, 2),
                   '>': Token(1, lambda x, y: x > y, 2),
                   '+': Token(2, lambda x, y: x + y, 2),
                   '-': Token(2, lambda x, y: x - y, 2),
                   '*': Token(3, lambda x, y: x * y, 2),
                   '/': Token(3, lambda x, y: x / y, 2),
                   '//': Token(3, lambda x, y: x // y, 2),
                   '%': Token(3, lambda x, y: x % y, 2),
                   '--': Token(4, lambda x: -x, 1),         #unary minus
                   '++': Token(4, lambda x: x, 1),          #unary plus
                   '^': Token(4, lambda x, y: x ** y, 2),
                   'abs': Token(5, lambda x: abs(x), None),
                   'round': Token(5, lambda x: round(x), None)})

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.result = []

    def is_float(self, x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    def parse(self):
        self.result = self.convert_to_rpn()
        return self.result

    def check_priority(self, token_1, token_2):
        #'--', '++', '^' - right associative operators
        return Parser.TOKENS[token_1].priority > Parser.TOKENS[token_2].priority if token_2 in ['--', '++', '^'] \
            else Parser.TOKENS[token_1].priority >= Parser.TOKENS[token_2].priority

    def convert_to_rpn(self, in_function = False):
        '''This method converts tokens to reverse polish notation.
        The result will be placed in self.result.'''

        result = []
        operators = []
        is_next_unary = True

        if in_function:
            operators.append('(')
    
        while self.position < len(self.tokens):
            current_token = self.tokens[self.position]
            if self.is_float(current_token):
                result.append(float(current_token))
                is_next_unary = False
    
            elif current_token in Lexer.CONSTANTS:
                result.append(Parser.TOKENS[current_token].function)
                is_next_unary = False
    
            elif current_token == '(':
                operators.append(current_token)
                is_next_unary = True

            elif current_token == ')':
                try:
                    current_operator = operators.pop()
                    while current_operator != '(':
                        result.append(current_operator)
                        current_operator = operators.pop()
                    is_next_unary = False
                    if not operators and in_function:      
                        return result
                except:
                    raise SyntaxError('ERROR: brackets are not balanced.')
    
            elif current_token in Lexer.OPERATORS:
                if is_next_unary:
                    if current_token == '+':
                        current_token = '++'
                    elif current_token == '-':
                        current_token = '--'
                    else:
                        raise SyntaxError('ERROR: invalid expression, %s cannot be unary!' % current_token)

                if operators:
                    current_operator = operators[-1]
                while operators and self.check_priority(current_operator, current_token):
                    result.append(current_operator)
                    operators.pop()
                    if operators:
                        current_operator = operators[-1]
                operators.append(current_token)

                is_next_unary = True
    
            elif current_token in Lexer.FUNCTIONS:
                current_token = current_token[ : -1]
                if operators:
                    current_operator = operators[-1]
                while operators and self.check_priority(current_operator, current_token):
                    result.append(current_operator)
                    operators.pop()
                    if operators:
                        current_operator = operators[-1]
                operators.append(current_token)
                self.position += 1
                result.append(self.convert_to_rpn(in_function = True))
                is_next_unary = False
    
            elif current_token == ',':
                if not in_function:
                    raise SyntaxError('ERROR: invalid expression. Unexpected token \',\'.')
                while len(operators) > 1:
                    if operators[-1] == '(':
                        raise SyntaxError('ERROR: invalid brackets.')
                    result.append(operators.pop())
                result.append(current_token)
                is_next_unary = True    

            self.position += 1
    
        while operators:
            if operators[-1] == '(':
                raise SyntaxError('ERROR: brackets are not balanced.')
            result.append(operators.pop())
    
        return result

def calculate(expression):
    '''This function calculates expression represented in reverse polish notation.'''

    result = []
    commas_number = 0
    for token in expression:
        if type(token) in [int, float, list]:
            result.append(token)
        elif token == ',':
            commas_number += 1
        else:
            try:
                if Parser.TOKENS[token].args_number == 2:
                    y, x = result.pop(), result.pop()
                    result.append(Parser.TOKENS[token].function(x, y))
                elif Parser.TOKENS[token].args_number == 1:
                    result.append(Parser.TOKENS[token].function(result.pop()))
                elif token == 'fsum':
                    result.append(Parser.TOKENS[token].function(calculate(result.pop())))
                else:
                    result.append(Parser.TOKENS[token].function(*calculate(result.pop())))
            except TypeError:
                raise SyntaxError('ERROR: invalid number of arguments \'' + token + '\'.')
            except IndexError:
                raise SyntaxError('ERROR: invalid expression.')
                
    if len(result) != commas_number + 1:
        raise SyntaxError('ERROR: invalid expression.')

    return result
            
if __name__ == '__main__':
    #parsing args
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    expression = parser.parse_args().EXPRESSION
    
    try:
        lexer = Lexer(expression)
        tokens = lexer.get_all_tokens()
        parser = Parser(tokens)
        parser.parse()
        print(parser.result)
        print(*calculate(parser.result))
    except SyntaxError as ex:
        print(ex)

