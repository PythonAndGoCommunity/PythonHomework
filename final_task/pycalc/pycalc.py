#!/usr/bin/env python3
"""Main module, that takes the command line argument and sends it on its way to verify and calculate."""
import sys
import pycalc.parse as parse
import pycalc.compexp as compexp
import pycalc.custom_exception as custom_exc
import pycalc.expproc as expproc
import pycalc.calcexp as calcexp


def main():
    """Main function of our python calculator"""
    args = sys.argv[1:]
    expression = parse.parse_argument(args)
    if expression == "":
        print("ERROR: empty string cannot be passed as argument.")
        sys.exit(1)
    try:
        comp_checked = compexp.check_for_comp(expression)
        if len(comp_checked) == 1:
            rpn_expression = expproc.verify_expression(expression)
            answer = calcexp.calculate_expression(rpn_expression)
            print(answer)
        else:
            rpn_expression_left = expproc.verify_expression(comp_checked[0])
            answer_left = calcexp.calculate_expression(rpn_expression_left)
            rpn_expression_right = expproc.verify_expression(comp_checked[1])
            answer_right = calcexp.calculate_expression(rpn_expression_right)
            return comp_checked[2](answer_left, answer_right)
    except (custom_exc.VerifyException, ValueError, ZeroDivisionError) as error:
        print(error.msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
