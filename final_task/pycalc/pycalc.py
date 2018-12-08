"""Entry point of pycalc project."""

from .argparser import Argparser
from .calculator import Calculator
from .validator import Validator


def main():
    argparser = Argparser()
    validator = Validator()

    args = argparser.parse_input()
    expression = args.expression[0]
    modules = args.modules
    calc = Calculator(validator, modules)
    result = calc.calc_start(expression)

    print(result)


if __name__ == "__main__":
    main()
