"""
This module allows you to work
with the functionality of calculator
"""
import arguments
from checker import (is_number, is_empty)
import operations


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
    answer = operations.is_inequality(arg.EXPRESSION)
    if answer is True:
        print(operations.solve_inequality(arg.EXPRESSION))
    else:
        print(operations.MathExp(arg.EXPRESSION).evaluate())


if __name__ == '__main__':
    main()
