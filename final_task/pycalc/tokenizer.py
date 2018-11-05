"""This module contains a class that allows to find and extract tokens from the user's mathematical expression"""

# general import 
import re
# import from pycalc self library
from .pycalclib import r_strings, operators, constants


class Tokenizer():
    """A model of tokenizer capable of finding and extracting tokens from string math expression"""
    def __init__(self, user_expr):
        """Initialize tokenizer"""
        self.user_expr = user_expr
        self.r_strings = r_strings
        self.operators = operators
        self.constants = constants
        self.error_msg = None
        self.tokens = []

    def is_number(self, token):
        """Determines whether token is a number"""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def consider_sub_signs(self, tokens):
        """Considers and replaces several subtraction signs when they follow each other"""
        index = 0
        while True:
            if tokens[index] == '-' and (tokens[index+1] == '-' or tokens[index+1] == '+'):
                tokens.pop(index), tokens.pop(index)
                tokens.insert(index, '+')
            elif tokens[index] == '+' and tokens[index+1] == '-':
                tokens.pop(index), tokens.pop(index)
                tokens.insert(index, '-')
            elif tokens[index] == '+' and tokens[index+1] == '+':
                tokens.pop(index), tokens.pop(index)
                tokens.insert(index, '+')
            else:
                index += 1
            if index < len(tokens)-2:
                continue
            else:
                break

    def check_first_tokens(self, tokens):
        """Check whether first two tokens are a negative number (negative constant)
        and replaces them by negative number if so"""
        if tokens[0] == '-' and (self.is_number(tokens[1]) or tokens[1] in self.constants):
            if self.is_number(tokens[1]):
                first_neg_token = str(float(tokens[1])*-1)
            else:
                first_neg_token = '-{}'.format(tokens[1])
            tokens.pop(0), tokens.pop(0)
            tokens.insert(0, first_neg_token)

    def extract_tokens(self):
        """Extracts tokens from string math expression"""
        got_token = False  # flag that switches to True every time some token has been found
        
        while len(self.user_expr) != 0:
            for r_string in self.r_strings:
                search_result = re.search(r''.join(r_string), self.user_expr)
                if search_result is not None:
                    if (search_result.group(0) == '-' and len(self.tokens) != 0
                            and self.tokens[-1] in (['('] + self.operators[2:])):
                            continue
                    self.user_expr = self.user_expr[search_result.end():]
                    if search_result.group(0) != ' ':
                        self.tokens.append(search_result.group(0))
                    got_token = True
                    break
                else:
                    continue
            if got_token is False:  # is True when an unknown sign / signs has been found
                self.error_msg = "ERROR: invalid syntax"
                break
            got_token = False  # if one of acceptable sign/signs has been found, switch flag back to False for
            # the next entrance to the 'for' loop

        if len(self.tokens) >= 2:
            self.consider_sub_signs(self.tokens)
            self.check_first_tokens(self.tokens)

        return self.tokens, self.error_msg


if __name__ == '__main__':     
    print("This module contains class that allows to extract tokens from math strings. For example: \n")
    test_string = '1---1*-5-sin(-3)'
    print("Math string: ", test_string)
    tokenizer = Tokenizer(test_string)
    tokens, error_msg = tokenizer.extract_tokens()
    if not error_msg:
        print('Extracted tokes: ', tokens) 
    else:
        print(error_msg)
