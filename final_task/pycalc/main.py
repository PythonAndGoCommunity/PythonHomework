"""
This module allows you to work
with the functionality of calculator
"""
from pycalc import arguments
from pycalc.checker import is_empty
from pycalc.operations import is_number, solve_inequality, MathExp, is_inequality
import sys


def validate(expression):
    is_empty(expression)
    is_number(expression)


def main():
    """
    Entry point to pycalc

    print calculated value
    """
    arg = arguments.parse_arguments()
    validate(arg.EXPRESSION)
    answer = is_inequality(arg.EXPRESSION)
    if answer is True:
        print(solve_inequality(arg.EXPRESSION))
    else:
        answer = MathExp(arg.EXPRESSION).evaluate()
        if str(answer).startswith('ERROR'):
            sys.exit(-1)
        print(answer)


if __name__ == '__main__':
    main()
