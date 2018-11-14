"""This module contains a class that allows to evaluate math expression in RPN"""

# import
from .pycalclib import operators_dict, functions_dict


class RPNcalculator:
    """A model of RPN math expression evaluator"""

    def __init__(self, rpn_tokens):
        """Initialize RPNcalculator object"""

        self.rpn_tokens = rpn_tokens
        self.error_msg = None
        self.operators_dict = operators_dict
        self.functions_dict = functions_dict
        self.stack = []

    def evaluate(self):
        """Evaluates math expression given in a form of RPN tokens"""
        for token in self.rpn_tokens:
            if token in self.operators_dict.keys():
                try:
                    op2, op1 = self.stack.pop(), self.stack.pop()
                except IndexError:
                    self.error_msg = 'ERROR: invalid syntax'
                    break
                if token in ['^', '**'] and (float(op1) < 0 and (not float(op2).is_integer())):  # check pow operation
                    self.error_msg = 'ERROR: negative number cannot be raised to a fractional power'
                    break
                try:
                    self.stack.append(self.operators_dict[token](op1, op2))
                except Exception as e:
                    self.error_msg = 'ERROR: {}'.format(e)
                    break
            elif token in self.functions_dict.keys():
                if self.functions_dict[token][0] == 1:
                    try:
                        op1 = self.stack.pop()
                    except IndexError:
                        self.error_msg = 'ERROR: invalid syntax'
                        break
                    if token == 'sqrt' and float(op1) < 0:  # check sqrt operation
                        self.error_msg = "ERROR: a root can't be extracted from a negative number"
                        break
                    try:
                        self.stack.append(self.functions_dict[token][1](op1))
                    except Exception:
                        self.error_msg = 'ERROR: incorrect use of {} function'.format(token)
                        break
                elif self.functions_dict[token][0] == 2:
                    try:
                        op2, op1 = self.stack.pop(), self.stack.pop()
                    except IndexError:
                        self.error_msg = 'ERROR: invalid syntax'
                        break
                    if token == 'pow' and (float(op1) < 0 and (not float(op2).is_integer())):  # check pow function
                        self.error_msg = 'ERROR: negative number cannot be raised to a fractional power'
                        break
                    try:
                        self.stack.append(self.functions_dict[token][1](op1, op2))
                    except Exception:
                        self.error_msg = 'ERROR: incorrect use of {} function'.format(token)
                        break
            else:
                self.stack.append(float(token))

        # final check of result and error message:
        if not self.error_msg and len(self.stack) == 1:
            result = self.stack.pop()
        elif not self.error_msg and len(self.stack) > 1:
            result = None
            self.error_msg = 'ERROR: invalid syntax'
        else:
            result = None

        return result, self.error_msg


if __name__ == "__main__":
    print("This module contains class that allows to evaluate math expression in form of RPN tokens. For example: \n")
    test_rpn = ['2', '3', '4', '*', '-', '2', '5', '/', '-']
    print('RPN tokens math expression: ', test_rpn)
    rpncalculator = RPNcalculator(test_rpn)
    result, error_msg = rpncalculator.evaluate()
    if not error_msg:
        print('Result: ', result)
    else:
        print(error_msg)
