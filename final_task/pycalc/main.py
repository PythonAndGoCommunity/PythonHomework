#!/usr/bin/env python3
"""
This module allows you to work
with the functionality of calculator
"""

import sys
from pycalc.core import args
from pycalc.core.calculator import calculator


def main():
    """
    Entry point to pycalc

    print calculated value
    """
    arguments = args.arg_parser()

    answer = calculator(arguments.EXPRESSION, arguments.MODULE)
    print(answer)
    if str(answer).startswith('ERROR'):
        sys.exit(-1)


if __name__ == '__main__':
    main()
