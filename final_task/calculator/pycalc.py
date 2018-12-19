from re import compile
from io import StringIO
from tokenize import generate_tokens
import math
from argparse import ArgumentParser
from numbers import Number
from collections import namedtuple


class UnbalancedParenthesesError(Exception):
    def __init__(self, message):
        super(UnbalancedParenthesesError, self).__init__(message)


class UnknownFunctionError(Exception):
    def __init__(self, message):
        super(UnknownFunctionError, self).__init__(message)

        
class RedundantParameterError(Exception):
    def __init__(self, message):
        super(RedundantParameterError, self).__init__(message)


class MissingParameterError(Exception):
    def __init__(self, message):
        super(MissingParameterError, self).__init__(message)


class UnknownSymbolError(Exception):
    def __init__(self, message):
        super(UnknownSymbolError, self).__init__(message)


class UnexpectedSpaceError(Exception):
    def __init__(self, message):
        super(UnexpectedSpaceError, self).__init__(message)


class RPN:
    """
    Reverse Polish notation converter and handler class
    """

    def __init__(self):
        self.stack, self.output, self.expression, self.tokens = [], [], '', []
        self.postfix_ops = {'!': self.factorial}
        self.prefix_ops = {a: getattr(math, a) for a in dir(math) if callable(getattr(math, a))}
        other_prefix_op = {
            'log': self.logarithm,
            'log2': self.logarithm_two,
            'log10': self.logarithm_ten,
            'pow': self.power,
            'sqrt': self.square_root,
            'ln': self.logarithm_e,
            'abs': abs,
            'round': round,
            'minus': self.unary_minus,
            'plus': self.unary_plus,
        }
        self.prefix_ops.update(other_prefix_op)
        sign = namedtuple('sign', 'priority action')
        self.signs = {
            '^': sign(4, self.power),
            '**': sign(4, self.power),
            '/': sign(3, self.divide),
            '//': sign(3, self.int_divide),
            '%': sign(3, self.division_rest),
            '*': sign(3, lambda digit1, digit2: digit1 * digit2),
            '+': sign(2, lambda digit1, digit2: digit1 + digit2),
            '-': sign(2, lambda digit1, digit2: digit1 - digit2),
            '(': sign(1, None),
            ')': sign(1, None),
            '<': sign(0, lambda digit1, digit2: digit1 < digit2),
            '<=': sign(0, lambda digit1, digit2: digit1 <= digit2),
            '=': sign(0, lambda digit1, digit2: digit1 == digit2),
            '==': sign(0, lambda digit1, digit2: digit1 == digit2),
            '!=': sign(0, lambda digit1, digit2: digit1 != digit2),
            '>=': sign(0, lambda digit1, digit2: digit1 >= digit2),
            '>': sign(0, lambda digit1, digit2: digit1 > digit2)
        }
        values = {attr: getattr(math, attr) for attr in dir(math) if isinstance(getattr(math, attr), Number)}
        self.const_values = values
        self.all_ops = {**self.postfix_ops, **self.prefix_ops, **self.signs}

    def clear_stack(self):
        """
        Clears class attribute 'stack'
        """
        self.stack = []

    @staticmethod
    def is_num(item):
        """
        Checks whether this token is number
        """
        try:
            float(item)
            return True
        except (ValueError, TypeError):
            pass
        return False

    @staticmethod
    def unary_minus(digit):
        """
        Changes 'digit' to '-digit'
        """
        return (-1) * digit

    @staticmethod
    def unary_plus(digit):
        """
        Changes 'digit' to '+digit'
        """
        return digit

    @staticmethod
    def factorial(digit):
        """
        Calculates factorial on a digit
        """
        if digit < 0:
            raise ValueError('can\'t count factorial of negative number')
        elif not str(digit).isdigit():
            raise ValueError('can\'t count factorial of fractional number')
        else:
            return math.factorial(digit)

    @staticmethod
    def logarithm(digit1, digit2):
        """
        Calculates logarithm of digit1 by base digit2
        """
        if digit2 == 1:
            raise ZeroDivisionError('cant\'t count logarithm by base 1')
        elif digit1 <= 0:
            raise ValueError('can\'t count non-positive logarithm')
        else:
            return math.log(digit1, digit2)

    @staticmethod
    def logarithm_e(digit):
        """
        Calculates natural logarithm of digit by base e
        """
        if digit > 0:
            return math.log(digit)
        else:
            raise ValueError('can\'t count non-positive logarithm')

    def resolve_log(self):
        """
        If log() takes two parameter leaves it the same
        If log() takes one parameter changes log() to ln() in place
        """
        open_parentheses_count = 0
        close_parentheses_count = 0
        for index, token in enumerate(self.tokens):
            if token == 'log':
                n_args = 1
                for new_token in self.tokens[index + 1:]:
                    if new_token == '(':
                        open_parentheses_count += 1
                    if new_token == ',':
                        n_args = 2
                    if new_token == ')':
                        close_parentheses_count += 1
                    if open_parentheses_count == close_parentheses_count:
                        break
                if n_args == 1:
                    self.tokens[index] = 'ln'

    @staticmethod
    def logarithm_two(digit):
        """
        Calculates logarithm of digit by base two
        """
        if digit > 0:
            return math.log2(digit)
        else:
            raise ValueError('can\'t count non-positive logarithm by base 2')

    @staticmethod
    def logarithm_ten(digit):
        """
        Calculates logarithm of digit by base ten
        """
        if digit > 0:
            return math.log10(digit)
        else:
            raise ValueError('can\'t count non-positive logarithm by base 10')

    @staticmethod
    def power(digit1, digit2):
        """
        Calculates digit2-power of digit1
        """
        if digit1 < 0 and not digit2.is_integer():
            raise ValueError('can\'t raise negative number to fractional power')
        else:
            return pow(digit1, digit2)

    @staticmethod
    def square_root(digit):
        """
        Calculates square root of digit
        """
        if digit >= 0:
            return math.sqrt(digit)
        else:
            raise ValueError('can\'t count square root of negative number')

    @staticmethod
    def divide(digit1, digit2):
        """
        Calculates digit1 divided by digit2
        """
        if digit2 == 0:
            raise ZeroDivisionError('can\'t divide by zero')
        else:
            return digit1 / digit2

    @staticmethod
    def int_divide(digit1, digit2):
        """
        Performes integer division of digit1 by digit2
        """
        if digit2 == 0:
            raise ZeroDivisionError('can\'t divide by zero')
        else:
            return digit1 // digit2

    @staticmethod
    def division_rest(digit1, digit2):
        """
        Calculates the rest of division of ditit1 by digit2
        """
        if digit2 == 0:
            raise ZeroDivisionError('can\'t divide by zero')
        else:
            return digit1 % digit2

    def add_implicit_multiply(self, tokens_list):
        """
        Adds implicit multiplication to the new tokens list
        Returns resolved list
        """
        resolved_list = []
        for index, token in enumerate(tokens_list):
            prev = tokens_list[index - 1]
            if index == 0:
                resolved_list.append(token)
            elif self.is_num(token) and prev == ')':
                resolved_list.append('*')
                resolved_list.append(token)
            elif token == '(' and prev == ')':
                resolved_list.append('*')
                resolved_list.append(token)
            elif token == '(' and self.is_num(prev):
                resolved_list.append('*')
                resolved_list.append(token)
            else:
                resolved_list.append(token)
        return resolved_list

    def resolve_unary(self, tokens_list):
        """
        Resolves all unary '-' and '+' operations changing them to 'minus' and 'plus' functions
        Returns resolved list
        """
        resolved_list = []
        for index, token in enumerate(tokens_list):
            prev = tokens_list[index - 1]
            if token == '-' or token == '+':
                if index == 0:
                    resolved_list.append('minus') if token == '-' else resolved_list.append('plus')
                elif prev == ')' or prev in self.const_values or self.is_num(prev):
                    resolved_list.append(token)
                else:
                    resolved_list.append('minus') if token == '-' else resolved_list.append('plus')
            else:
                resolved_list.append(token)
        return resolved_list

    @staticmethod
    def create_tokens_list(some_string):
        """
        Creates tokens list from math expressions string
        """
        line = generate_tokens(StringIO(some_string).readline)
        return [token[1] for token in line if token[1]]

    def convert_to_rpn(self, text):
        """
        Converts initial math expression to Reverse Polish Notation while solving log(), unary operation
        and adds implicit multiplication
        Return tokens list in Reverse Polish Notation
        """
        self.tokens = self.create_tokens_list(text)
        self.resolve_log()
        self.tokens = self.resolve_unary(self.tokens)
        self.tokens = self.add_implicit_multiply(self.tokens)
        for item in self.tokens:
            if self.is_num(item) or item in self.postfix_ops or item in self.const_values:
                self.output.append(item)
            elif item == '(' or item in self.prefix_ops:
                self.stack.append(item)
            elif item == ')':
                for element in reversed(self.stack):
                    if element != '(':
                        self.output.append(self.stack.pop())
                    else:
                        self.stack.pop()
                        break
            elif item in self.signs:
                for element in reversed(self.stack):
                    if self.stack[-1] in self.prefix_ops \
                            or self.signs[self.stack[-1]].priority > self.signs[item].priority \
                            or self.signs[self.stack[-1]].priority == self.signs[item].priority and item != '^':
                        self.output.append(self.stack.pop())
                self.stack.append(item)
            elif item == ',':
                for element in reversed(self.stack):
                    if element != '(':
                        self.output.append(self.stack.pop())
                    else:
                        break
            else:
                raise UnknownFunctionError(f'wrong operation "{item}"')
        for element in reversed(self.stack):
            self.output.append(self.stack.pop())
        self.clear_stack()
        return list(self.output)

    def pop_one(self):
        """
        Pops one item from stack
        """
        return float(self.stack.pop())

    def pop_two(self):
        """
        Pops two items from stack
        """
        y = float(self.stack.pop())
        x = float(self.stack.pop())
        return x, y

    def handle_operations(self, rpn_expression):
        """
        Handles all operations in RPN tokens list
        Return result of calculation
        """
        for op in rpn_expression:
            # print('Stack: ', self.stack)
            if op in self.const_values:
                self.stack.append(self.const_values[op])
            elif op not in self.all_ops:
                self.stack.append(op)
            elif op in self.signs:
                try:
                    function = self.signs[op].action
                    x, y = self.pop_two()
                    self.stack.append(function(x, y))
                except IndexError:
                    raise MissingParameterError(f'not enough operands for "{op}" operation')
            elif op in self.prefix_ops or self.postfix_ops:
                try:
                    if op in ('fmod', 'gcd', 'isclose', 'ldexp', 'remainder', 'log', 'pow', 'atan2'):
                        function = self.all_ops[op]
                        x, y = self.pop_two()
                        self.stack.append(function(x, y))
                    else:
                        function = self.all_ops[op]
                        self.stack.append(function(self.pop_one()))
                except IndexError:
                    raise MissingParameterError(f'not enough operands for "{op}" operation')
        if len(self.stack) > 1:
            raise RedundantParameterError('function takes more parameters that it should')
        return self.stack[0]

    @staticmethod
    def parse_expression():
        """
        Creates command-line arguments parser
        Returns parsed argument
        """
        parser = ArgumentParser(description='Pure Python command-line calculator')
        parser.add_argument('EXPRESSION', help='expression string to evaluate', action='store_true')
        parsed, args = parser.parse_known_args()
        return args[0]


class Check(RPN):
    def __init__(self):
        super(Check, self).__init__()

    def check_for_numbers(self, text):
        """
        Checks whether expression has no operands
        :param text: initial math expression
        """
        tokens = self.create_tokens_list(text)
        numbers_count = 0
        for token in tokens:
            if self.is_num(token) or token in self.const_values:
                numbers_count += 1
        if numbers_count == 0:
            raise MissingParameterError('no numbers or constants in expression')

    @staticmethod
    def check_parentheses(text):
        """
        Checks whether parentheses are balanced
        """
        n = abs(text.count('(') - text.count(')'))
        if text.count('(') > text.count(')'):
            raise UnbalancedParenthesesError(f'expression has {n} unclosed parentheses')
        elif text.count('(') < text.count(')'):
            raise UnbalancedParenthesesError(f'expression has {n} redundant closing parentheses')
        if n == 0:
            pass

    @staticmethod
    def check_for_symbols(some_string):
        """
        Checks whether unsupported symbols are in the string
        """
        regex = compile('[;@_#$&?|}{~":]')
        if regex.search(some_string):
            raise UnknownSymbolError(f'unknown symbols "{regex.search(some_string).group()}"')
        else:
            pass

    @staticmethod
    def check_spaces(some_string):
        """
        Checks whether unexpected spaces are in the string
        """
        for index, char in enumerate(some_string):
            try:
                nxt = some_string[index + 1]
                prev = some_string[index - 1]
                if char == ' ':
                    if nxt.isdigit() and prev.isdigit():
                        raise UnexpectedSpaceError('unexpected space between numbers')
                    elif nxt == ' ' or prev == ' ':
                        raise UnexpectedSpaceError('unexpected double space')
                    elif nxt == '.' and prev.isdigit() or nxt.isdigit() and prev == '.':
                        raise UnexpectedSpaceError('unexpected space between/or in fractional numbers')
                    elif nxt in '<>=!' and prev in '<>=!':
                        raise UnexpectedSpaceError(f'unexpected space in comparison operation {prev + nxt}')
                    elif nxt in '*/^' and prev in '*/^':
                        raise UnexpectedSpaceError(f'unexpected space in operation {prev + nxt}')
                    elif prev == '(' and nxt == ')':
                        raise UnexpectedSpaceError('unexpected empty parentheses')
                    elif prev == ')' and nxt == '.':
                        raise UnexpectedSpaceError('unexpected fractional number after ")"')
            except IndexError:
                pass

    def initial_check(self, expression):
        """
        Performes initial checks of the expression for errors
        """
        self.check_parentheses(expression)
        self.check_for_symbols(expression)
        self.check_for_numbers(expression)
        self.check_spaces(expression)


def main():
    try:
        rpn = RPN()
        check = Check()
        rpn.expression = rpn.parse_expression()
        check.initial_check(rpn.expression)
        rpn_expression = rpn.convert_to_rpn(rpn.expression)
        print(rpn.handle_operations(rpn_expression))
    except Exception as e:
        print(f'ERROR: {e}')


if __name__ == "__main__":
    main()
