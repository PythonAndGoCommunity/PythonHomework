#!/usr/bin/env python3
"""Module for processing expression with comparison operators"""
import pycalc.custom_exception as custom_exc
import operator

comparison_dictionary = {">=": operator.ge, "<=": operator.le,
                         "==": operator.eq, "!=": operator.ne,
                         "<": operator.lt, ">": operator.gt}


def check_for_comp(expression):
    """This function checks number of comparison operators in our expression and
    returns either our expression, or a list, where 2 first elements are left and
    right parts of expression and 3-rd element is comparison operator"""
    found = False
    split_expression = []
    tmp_expression = expression
    found_operator = ""
    comparison_operators = comparison_dictionary.keys()
    for op in comparison_operators:
        tmp_list = tmp_expression.split(op)
        if len(tmp_list) > 2 or (len(tmp_list) == 2 and found):
            raise custom_exc.VerifyError("""ERROR: number of comparison operators is more than 1.""")
        elif len(tmp_list) == 2:
            found = True
            split_expression = tmp_list
            found_operator = op
            tmp_expression = tmp_expression.replace(op, ' ')
    if found:
        split_expression.append(comparison_dictionary[found_operator])
        return split_expression
    else:
        return [expression]
