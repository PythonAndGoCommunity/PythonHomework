"""This module contains a class that allows to replace constants with their numeric equivalents"""

from .pycalclib import Pycalclib


class Constsreplacer:
    """A model of constants replacer capable of replacing constants (from math module) by their numeric equivalents"""

    def __init__(self, rpn_tokens, pycalclib):
        """Initialize constsreplacer"""
        self.rpn_tokens = rpn_tokens
        self.constants_numeric_equivalents = pycalclib.constants_numeric_equivalents

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
    pycalclib = Pycalclib(user_module='')
    constsreplacer = Constsreplacer(test_tokens, pycalclib)
    rpn_tokens = constsreplacer.replace_constants()
    print('RPN tokens after replacement of constants: ', rpn_tokens)
