"""
This module allows you to work
with the functionality of calculator
"""
from pycalc import arguments
from pycalc import checker
from pycalc import operations


def validate(expression):
    checker.is_empty(expression)
    checker.is_number(expression)


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
