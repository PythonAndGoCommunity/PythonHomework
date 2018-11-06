"""This module contains a class that allows to take into account implicit multiplication signs"""

# import from pycalc self library
from .pycalclib import constants, functions, negative_functions


class Multsignsadder():
    """A model of mult_signs_adder capable of adding implicit multiplications signs in list of tokens"""

    def __init__(self, tokens):
        """Initialize mult_signs_adder"""
        self.tokens = tokens
        self.extended_tokens = []
        self.constants = constants
        self.functions = functions
        self.negative_functions = negative_functions

    def is_number(self, token):
        """Determines whether token is a number"""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def consider_neg_functions(self, tokens):
        """Replaces negative functions tokens by '-1*function' tokens"""
        index = 0
        while index != len(tokens)-1:
            if tokens[index] in self.negative_functions:
                tokens[index] = tokens[index][1:]  # remove '-' sign
                tokens.insert(index, '-1')
                tokens.insert(index+1, '*')
                index += 3
            index += 1

    def consider_log_args(self, tokens):
        """Adds 'e' as a base for log function explicitly if last was originally entered with one argument"""
        for index in range(len(tokens)):
            if tokens[index] == 'log':
                for index2 in range(index+1, len(tokens)):
                    if ((tokens[index2] == ')' and index2 == len(tokens)-1)
                            or (tokens[index2] == ')' and index2 != len(tokens)-1 and tokens[index2+1] != ',')):
                        log_args = tokens[index+2:index2]
                        if ',' not in log_args:
                            tokens.insert(index2, ',')
                            tokens.insert(index2+1, 'e')
                            break

    def addmultsigns(self):
        """Adds implicit multiplication signs in list of math tokens to where they are supposed to be"""
        for index in range(len(self.tokens)-1):
            self.extended_tokens.append(self.tokens[index])
            if (self.is_number(self.tokens[index]) and ((self.tokens[index+1] in self.constants)
                                                        or (self.tokens[index+1] in self.functions)
                                                        or (self.tokens[index+1] == '('))):
                self.extended_tokens.append('*')
                continue
            elif self.tokens[index] == ')' and self.tokens[index+1] == '(':
                self.extended_tokens.append('*')
                continue
        self.extended_tokens.append(self.tokens[-1])

        self.consider_neg_functions(self.extended_tokens)
        self.consider_log_args(self.extended_tokens)

        return self.extended_tokens


if __name__ == '__main__':
    print("""This module contains class that allows to insert multiplications signs to where they where supposed
    to be in a list with math tokens. For example: \n""")
    test_tokens = ['-0.1', 'tan', '+', '23', '*', '-sin', '(', '3', ')', '/', '.12', 'e']
    mult_signs_adder = Multsignsadder(test_tokens)
    extended_tokens = mult_signs_adder.addmultsigns()
    print('Original tokens: ', test_tokens)
    print('Extended tokens: ', extended_tokens)
