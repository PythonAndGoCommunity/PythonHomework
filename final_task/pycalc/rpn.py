"""This module contains a class that allows to transform infix notation math tokens into RPN"""

# import
from .pycalclib import constants, negative_constants, operators, comparison_operators, precedence
from .pycalclib import functions, negative_functions


class RPN:
    """A model of rpn capable of converting infix to postfix (RPN) notation"""

    def __init__(self, tokens):
        """Initialize rpn"""
        self.tokens = tokens
        self.operators_stack = []
        self.output_queue = []
        self.error_msg = None
        self.constants = constants
        self.negative_constants = negative_constants
        self.operators = operators
        self.comparison_operators = comparison_operators
        self.precedence = precedence
        self.functions = functions
        self.negative_functions = negative_functions

    @staticmethod
    def is_left_associative(operator):
        """Determines whether operator is left associative"""
        if operator in ['^', '**']:
            return False
        else:
            return True

    def is_number(self, token):
        """Determines whether token is a number"""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def convert2rpn(self):
        """Converts list of tokens in infix notation into RPN"""
        counter = 0
        while counter != (len(self.tokens)):
            current_token = self.tokens[counter]
            if self.is_number(current_token) or (current_token in (self.constants + self.negative_constants)):
                self.output_queue.append(current_token)
                counter += 1
            elif current_token in self.functions or current_token in self.negative_functions:
                self.operators_stack.append(current_token)
                counter += 1
            elif current_token in self.operators or current_token in self.comparison_operators:
                if len(self.operators_stack) == 0:
                    self.operators_stack.append(current_token)
                    counter += 1
                else:
                    while (len(self.operators_stack) != 0
                           and ((self.operators_stack[-1] in self.functions
                                 or self.operators_stack[-1] in self.negative_functions)
                                or (self.precedence[self.operators_stack[-1]] > self.precedence[current_token])
                                or (self.precedence[self.operators_stack[-1]] == self.precedence[current_token]
                                    and self.is_left_associative(self.operators_stack[-1])))
                           and (self.operators_stack[-1] != "(")):
                        self.output_queue.append(self.operators_stack.pop())
                    self.operators_stack.append(current_token)
                    counter += 1
            elif current_token == '(':
                self.operators_stack.append(current_token)
                counter += 1
            elif current_token in [')', ',']:
                if len(self.operators_stack) == 0 and len(self.output_queue) == 0:
                    if current_token == ')':
                        self.error_msg = "ERROR: brackets are not balanced"
                    elif current_token == ',':
                        self.error_msg = "ERROR: incorrect usage of ','"
                    break
                elif len(self.operators_stack) == 0 and len(self.output_queue) != 0:
                    if current_token == ')':
                        self.error_msg = "ERROR: brackets are not balanced"
                    elif current_token == ',':
                        self.error_msg = "ERROR: incorrect usage of ','"
                    break
                else:
                    while len(self.operators_stack) != 0:
                        if self.operators_stack[-1] != '(':
                            self.output_queue.append(self.operators_stack.pop())
                        else:
                            if current_token == ')':
                                self.operators_stack.pop()  # it should be '('
                            counter += 1
                            break
                    else:
                        self.error_msg = "ERROR: brackets are not balanced"
                        break
        if not self.error_msg:
            # if there are tokens left in operators_stack consistently add them to output_queue
            while self.operators_stack:
                remaining_operator = self.operators_stack.pop()
                if remaining_operator not in ['(', ')']:
                    self.output_queue.append(remaining_operator)
                else:
                    self.error_msg = 'ERROR: brackets are not balanced'

        return self.output_queue, self.error_msg


if __name__ == '__main__':
    print("""This module contains class that allows to transform a list of math tokens in infix notation into list of
tokens in RPN. For example: \n""")
    test_tokens = ['-pi', '*', 'round', '(', '2.23', ')', '//', '5', '*', 'pow', '(', '2', '3', ')']
    print("Infix_tokens: ", test_tokens)
    rpn = RPN(test_tokens)
    rpn_tokens, error_msg = rpn.convert2rpn()
    if not error_msg:
        print('RPN tokens: ', rpn_tokens)
    else:
        print(error_msg)
