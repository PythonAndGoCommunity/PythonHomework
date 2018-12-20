"""
This module allows you to work
with the functionality of calculator
"""
from pycalc.arguments import parse_arguments
from pycalc.operations import (is_number, solve_inequality,
    MathExp, is_inequality, parens_are_balanced, is_logwith2args, is_pow)
import sys


def is_empty(expr):
    if not expr:
        raise Exception("ERROR: Your expression is empty")


def validate(expression):
    is_empty(expression)
    is_number(expression)
    parens_are_balanced(expression)


def main():
    """
    Entry point to pycalc

    print calculated value
    """
    arg = parse_arguments()

    validate(arg.EXPRESSION)
    expression = arg.EXPRESSION
    expression = is_logwith2args(expression)
    expression = is_pow(expression)
    expression = expression.replace(" ", "")
    answer = is_inequality(expression)
    if answer is True:
        print(solve_inequality(expression))
    else:
        answer = MathExp(expression).evaluate()
        if str(answer).startswith('ERROR'):
            sys.exit(-1)
        print(answer)


if __name__ == '__main__':
    main()
