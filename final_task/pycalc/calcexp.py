#!/usr/bin/env python3
"""Module, that calculates our expression"""
import math
import operator
import pycalc.mydict as mydict

operations_2 = {"-": operator.sub, "+": operator.add, "*": operator.mul, "^": operator.pow,
                "/": operator.truediv, "//": operator.floordiv, "%": operator.mod,
                "log": math.log, "pow": math.pow, "round2": round}
operations_1 = {"exp": math.exp, "log2": math.log2, "log10": math.log10, "sin": math.sin,
                "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos,
                "atan": math.atan, "abs": abs, "neg": operator.neg, "pos": operator.pos,
                "round1": round, "loge": math.log}
constants = {"pi": math.pi, "e": math.e}
my_operations_2 = mydict.MyDict(operations_2)
my_operations_1 = mydict.MyDict(operations_1)
my_constants = mydict.MyDict(constants)
del operations_1
del operations_2
del constants


def calculate_expression(expression):
    """Function, that splits our expression in reverse polish notation
    into tokens(with help of our verify function) and then calculates it."""
    token_list = expression.split(" ")
    operands_stack = []
    size = len(token_list)
    for i in range(size):
        if token_list[i] == "":
            continue
        if token_list[i].isdigit():
            operands_stack.append(int(token_list[i]))
            continue
        if token_list[i].replace('.', '', 1).isdigit():
            operands_stack.append(float(token_list[i]))
            continue
        try:
            if my_operations_1[token_list[i]] != -1:
                if len(operands_stack) >= 1:
                    operands_stack.append(my_operations_1[token_list[i]](operands_stack.pop()))
                else:
                    return """ERROR: it seems there is a mistake in expression.
                    For example: 2 adjoining operators."""
                continue
            if my_operations_2[token_list[i]] != -1:
                if len(operands_stack) >= 2:
                    number1 = operands_stack.pop()
                    number2 = operands_stack.pop()
                    tmp = my_operations_2[token_list[i]](number2, number1)
                    if type(tmp) == complex:
                        return """ERROR: negative number cannot be raised to a fractional power."""
                    else:
                        operands_stack.append(tmp)
                else:
                    return """ERROR: it seems there is a mistake in expression.
                    For example: 2 adjoining operators."""
                continue
            if my_constants[token_list[i]] != -1:
                operands_stack.append(my_constants[token_list[i]])
                continue
        except ZeroDivisionError:
            return """ERROR: number cannot be divided by 0."""
    answer = operands_stack.pop()
    if len(operands_stack) != 0:
        return "ERROR: missing operator somewhere."
    return answer
