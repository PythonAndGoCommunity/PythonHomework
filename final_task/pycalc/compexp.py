#!/usr/bin/env python3
"""Module for processing expression with comparison operators"""
import pycalc.expproc as expproc
import operator

comparison_dictionary = {">=": operator.ge, "<=": operator.le,
                         "==": operator.eq, "!=": operator.ne,
                         "<": operator.lt, ">": operator.gt}


def check_for_comp(expression):
    """This function checks number of comparison operators in our expression."""
    found = False
    split_expression = []
    tmp_expression = expression
    found_operator = ""
    comparison_operators = comparison_dictionary.keys()
    for op in comparison_operators:
        tmp_list = tmp_expression.split(op)
        if len(tmp_list) > 2 or (len(tmp_list) == 2 and found):
            return "ERROR: number of comparison operators is more than 1."
        elif len(tmp_list) == 2:
            found = True
            split_expression = tmp_list
            found_operator = op
            tmp_expression = tmp_expression.replace(op, ' ', 1)
    if not found:
        answer = expproc.verify_expression(expression)
        return answer
    else:
        answer_list = []
        for expression in split_expression:
            if expression == "":
                return "ERROR: one side of inequality is empty."
            answer = expproc.verify_expression(expression)
            if type(answer) == str:
                return answer
            else:
                answer_list.append(answer)
        real_operator = comparison_dictionary[found_operator]
        answer = real_operator(answer_list[0], answer_list[1])
        return answer
