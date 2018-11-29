#!/usr/bin/env python3
"""Module, that first verifies the expression, splits it into tokens and then, if it's valid,
 sends it to calculate_expression for calculation"""
import pycalc.dictwithmissing as dictwithmissing
import pycalc.custom_exception as custom_exc


operations = {"-": 4, "+": 4, "*": 3, "^": 1, "/": 3, "//": 3, "%": 3,
              "exp": 0, "log": 0, "log2": 0, "log10": 0, "sin": 0,
              "cos": 0, "tan": 0, "cot": 0, "asin": 0, "acos": 0,
              "atan": 0, "abs": 0, "neg": 2, "pos": 2, "round": 0,
              "pow": 0}
unary_operations = {"-": "neg", "+": "pos"}
multifuncs_basic = ["round", "log", "pow"]
multifuncs_table = {("round", True): "round2", ("round", False): "round1", ("log", True): "log",
                    ("log", False): "loge", ("pow", True): "pow"}
missdict_unary_operations = dictwithmissing.DictWithMissing(unary_operations)
operations_to_stack = dictwithmissing.DictWithMissing(operations)
missdict_multifuncs_table = dictwithmissing.DictWithMissing(multifuncs_table)
constants = ["pi", "e"]
del operations
del unary_operations
del multifuncs_table


def verify_expression(expression):
    """This function converts our infix expression into reverse polish
    notation and at the same time checks it for brackets' balance and splits
    it into tokens with spaces"""
    token_list = []
    stack_operations = []
    multifunc_flags = []
    prev_token = ""
    i = 0
    length = len(expression)
    while i < length:
        if expression[i] == " ":
            token_list.append(" ")
            i += 1
            continue
        if expression[i].isdigit() or expression[i] == ".":
            token_list.append(expression[i])
            prev_token = expression[i]
            i += 1
            continue
        if missdict_unary_operations[expression[i]] != -1:
            if i == 0:
                stack_operations.append(missdict_unary_operations[expression[i]])
                prev_token = expression[i]
                i += 1
                continue
            elif not prev_token.isdigit() and\
                    prev_token != "pi" and\
                    prev_token != "e" and\
                    prev_token != ")":
                stack_operations.append(missdict_unary_operations[expression[i]])
                prev_token = expression[i]
                i += 1
                continue
        if expression[i] == "(":
            stack_operations.append("(")
            token_list.append(" ")
            prev_token = expression[i]
            i += 1
            continue
        if expression[i] == ")":
            token_list.append(" ")
            prev_token = ")"
            finished = False
            while len(stack_operations) != 0 and not finished:
                tmp = stack_operations.pop()
                finished = tmp == "("
                if not finished:
                    token_list.append(tmp)
                    token_list.append(" ")
            if not finished:
                raise custom_exc.VerifyError("""ERROR: equilibrium of parentheses is violated.
                Redundant closing parentheses found.""", i)
            else:
                i += 1
            continue
        if expression[i] == ",":
            token_list.append(" ")
            if not multifunc_flags.pop():
                multifunc_flags.append(True)
            else:
                raise custom_exc.VerifyError("""ERROR: there is a comma sitting lonely...""", i)
            prev_token = ","
            finished = False
            while len(stack_operations) != 0 and not finished:
                tmp = stack_operations.pop()
                finished = tmp == "("
                if not finished:
                    token_list.append(tmp)
                    token_list.append(" ")
                else:
                    stack_operations.append("(")
            if not finished:
                raise custom_exc.VerifyError("""ERROR: something wrong in two-argument
                function.""", i)
            else:
                i += 1
            continue
        found = False
        for x in range(5, 0, -1):  # I know, it's a bad style coding, i just couldn't think of a better solution
            token = expression[i:i+x]
            if operations_to_stack[token] != -1:
                found = True
                if operations_to_stack[token] == 0:
                    stack_operations.append(token)
                    if token in multifuncs_basic:
                        multifunc_flags.append(False)
                else:
                    token_list.append(" ")
                    size = len(stack_operations)
                    if size != 0:
                        while operations_to_stack[stack_operations[size - 1]] != -1 and (
                              operations_to_stack[stack_operations[size - 1]] < operations_to_stack[token] or (
                               operations_to_stack[stack_operations[size - 1]] == operations_to_stack[token] and
                               token != "^")):
                            tmp_op = stack_operations.pop()
                            if tmp_op in multifuncs_basic:
                                if len(multifunc_flags) == 0:
                                    raise custom_exc.VerifyError("""ERROR: ?????""")
                                token_list.append(missdict_multifuncs_table[(tmp_op, multifunc_flags.pop())])
                            else:
                                token_list.append(tmp_op)
                            token_list.append(" ")
                            size -= 1
                            if size == 0:
                                break
                    stack_operations.append(token)
                i += x
                prev_token = token
                break
        if found:
            continue
        for x in constants:
            if expression[i:i+len(x)] == x:
                found = True
                token_list.append(x)
                token_list.append(" ")
                i += len(x)
                prev_token = x
                break
        if found:
            continue
        raise custom_exc.VerifyError("""ERROR: Unknown symbol found.""", i)
    token_list.append(" ")
    while len(stack_operations) != 0:
        tmp = stack_operations.pop()
        if tmp == "(":
            raise custom_exc.VerifyError("""ERROR: equilibrium of parentheses is violated.
            Missing closing parentheses.""")
        if tmp in multifuncs_basic:
            if len(multifunc_flags) == 0:
                raise custom_exc.VerifyError("""ERROR: ?????""")
            token_list.append(missdict_multifuncs_table[(tmp, multifunc_flags.pop())])
        else:
            token_list.append(tmp)
        token_list.append(" ")
    reverse_expression = ''.join(token_list)
    return reverse_expression
