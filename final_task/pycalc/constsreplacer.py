"""This module contains a class that allows to replace constants by their numeric equivalents"""

# import from pyalc self library
from .pycalclib import constants_numeric_equivalents


class Constsreplacer():
    """A model of constants replacer capable of replacing constants (from math module) by their numeric equivalents"""

    def __init__(self, rpn_tokens):
        """Initialize constsreplacer"""
        self.rpn_tokens = rpn_tokens
        self.constants_numeric_equivalents = constants_numeric_equivalents

    def replace_constants(self):
        """Replaces tokens which are math module constants by their numeric equivalent"""
        for index in range(len(self.rpn_tokens)):
            if self.rpn_tokens[index] in self.constants_numeric_equivalents.keys():
                self.rpn_tokens[index] = str(self.constants_numeric_equivalents[self.rpn_tokens[index]])

        return self.rpn_tokens


if __name__ == '__main__':
    print("""This module contains class that allows to replace tokens which are math module constants by their
    numeric equivalents. For example: \n""")
    test_tokens = ['2', '*', 'nan', '-', '-inf', '+', '-tau', '*', '-pi', '+', 'e']
    print('RPN tokens with constants: ', test_tokens)
    constsreplacer = Constsreplacer(test_tokens)
    rpn_tokens = constsreplacer.replace_constants()
    print('RPN tokens after replacement of constants: ', rpn_tokens)
