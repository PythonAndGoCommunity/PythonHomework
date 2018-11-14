#! /usr/bin/python3

# import
import argparse
import sys
from .tokenizer import Tokenizer
from .addmultsigns import Multsignsadder
from .rpn import RPN
from .constsreplacer import Constsreplacer
from .rpncalculator import RPNcalculator


def create_parser():
    """Creates parser with one positional argument 'expression' to parse user's mathematical expression"""
    parser = argparse.ArgumentParser(prog='pycalc', description='pure Python command line calculator',
                                     epilog="""Anton Charnichenka for EPAM: Introduction to Python
                                     and Golang programming, 2018.""")
    parser.add_argument('expression', help="""mathematical expression string to evaluate;
    implicit multiplication is supported""")

    return parser


def main():
    """Calculate user's expression"""
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    user_expr = namespace.expression

    # calculation chain
    # tokenize user's expression string
    tokenizer = Tokenizer(user_expr)
    tokens, error_msg = tokenizer.extract_tokens()
    if error_msg:
        print(error_msg)
        sys.exit(1)
    elif not tokens:
        print('ERROR: no expression was entered')
        sys.exit(1)
    # add implicit multiplication signs to the list of extracted tokens
    mult_signs_adder = Multsignsadder(tokens)
    tokens = mult_signs_adder.addmultsigns()
    # transform extracted tokens into RPN
    rpn = RPN(tokens)
    rpn_tokens, error_msg = rpn.convert2rpn()
    if error_msg:
        print(error_msg)
        sys.exit(1)
    # replace constants with their numeric equivalents
    constsreplacer = Constsreplacer(rpn_tokens)
    rpn_tokens = constsreplacer.replace_constants()
    # evaluate user's expression
    rpncalculator = RPNcalculator(rpn_tokens)
    result, error_msg = rpncalculator.evaluate()
    if error_msg:
        print(error_msg)
        sys.exit(1)
    else:
        print(result)
        sys.exit(0)


# main
if __name__ == "__main__":
    main()
