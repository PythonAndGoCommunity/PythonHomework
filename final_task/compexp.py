#!/usr/bin/env python3
"""Module for processing expression with comparison operators"""
import expproc
import operator

comparison_dictionary = {">=": operator.ge, "<=": operator.le,
                         "==": operator.eq, "!=": operator.ne,
                         "<": operator.lt, ">": operator.gt}


def check_for_comp(expression):
    """This function checks number of comparison operators in our expression."""
    found = False
    split_expression = []
    found_operator = ""
    comparison_operators = comparison_dictionary.keys()
    for op in comparison_operators:
        tmp_list = expression.split(op)
        if len(tmp_list) > 2 or (len(tmp_list) == 2 and found):
            return "ERROR: number of comparison operators is more than 1."
        elif len(tmp_list) == 2:
            found = True
            split_expression = tmp_list
            found_operator = op
    if found_operator == "":
        answer = expproc.verify_expression(expression)
        return answer
    else:
        answer_list = []
        for expression in split_expression:
            answer = expproc.verify_expression(expression)
            if type(answer) == str:
                return answer
            else:
                answer_list.append(answer)
        real_operator = comparison_dictionary[found_operator]
        answer = real_operator(answer_list[0], answer_list[1])
        return answer
