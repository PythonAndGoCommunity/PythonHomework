#!/usr/bin/env python3
"""Module, that calculates our expression"""
import math
import operator
import pycalc.dictwithmissing as dictwithmissing
import pycalc.custom_exception as custom_exc

operations_2arguments = {"-": operator.sub, "+": operator.add, "*": operator.mul, "^": operator.pow,
                         "/": operator.truediv, "//": operator.floordiv, "%": operator.mod,
                         "log": math.log, "pow": math.pow, "round2": round}
operations_1argument = {"exp": math.exp, "log2": math.log2, "log10": math.log10, "sin": math.sin,
                        "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos,
                        "atan": math.atan, "abs": abs, "neg": operator.neg, "pos": operator.pos,
                        "round1": round, "loge": math.log}
constants = {"pi": math.pi, "e": math.e}
missdict_operations_2arguments = dictwithmissing.DictWithMissing(operations_2arguments)
missdict_operations_1argument = dictwithmissing.DictWithMissing(operations_1argument)
missdict_constants = dictwithmissing.DictWithMissing(constants)
del operations_1argument
del operations_2arguments
del constants


def calculate_expression(expression):
    """Function, that splits our expression in reverse polish notation
    into tokens(with the help of our verify function putting spaces everywhere) and then calculates it."""
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
            if missdict_operations_1argument[token_list[i]] != -1:
                if operands_stack:
                    operands_stack.append(missdict_operations_1argument[token_list[i]](operands_stack.pop()))
                else:
                    raise custom_exc.VerifyError("""ERROR: it seems there is a mistake in expression.
                    For example: 2 adjoining operators.""")
                continue
            if missdict_operations_2arguments[token_list[i]] != -1:
                if len(operands_stack) >= 2:
                    number1 = operands_stack.pop()
                    number2 = operands_stack.pop()
                    tmp = missdict_operations_2arguments[token_list[i]](number2, number1)
                    if type(tmp) == complex:
                        raise ValueError("""ERROR: negative number
                         cannot be raised to a fractional power.""")
                    else:
                        operands_stack.append(tmp)
                else:
                    raise custom_exc.VerifyError("""ERROR: it seems there is a mistake in expression.
                    For example: 2 adjoining operators.""")
                continue
            if missdict_constants[token_list[i]] != -1:
                operands_stack.append(missdict_constants[token_list[i]])
                continue
        except ZeroDivisionError:
            raise ZeroDivisionError("""ERROR: number cannot be divided by 0.""")
    answer = operands_stack.pop()
    if operands_stack:
        raise custom_exc.VerifyError("""ERROR: missing operator somewhere.""")
    return answer
