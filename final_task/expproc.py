#!/usr/bin/env python3
"""Module, that first verifies the expression, splits it into tokens and then, if it's valid,
 sends it to calculate_expression for calculation"""
import calcexp
import mydict


class VerifyException(Exception):
    """Created a custom exception for handling errors right on
    place instead of using 100000 breaks and flags
    """
    def __init__(self, msg, position=None):
        if position is not None:
            msg = "{0} Position - {1}".format(msg, position)
        else:
            super(VerifyException, self).__init__(msg)
        self.msg = msg


operations = {"-": 4, "+": 4, "*": 3, "^": 1, "/": 3, "//": 3, "%": 3,
              "exp": 0, "log": 0, "log2": 0, "log10": 0, "sin": 0,
              "cos": 0, "tan": 0, "cot": 0, "asin": 0, "acos": 0,
              "atan": 0, "abs": 0, "neg": 2}
operations_to_stack = mydict.MyDict(operations)
operations_to_calculate = ["round", "pow"]
constants = ["pi", "e"]
del operations


def verify_expression(expression):
    """This function converts our infix expression into reverse polish
    notation and at the same time checks it for brackets' balance and splits
    it into tokens with spaces"""
    token_list = []
    stack_operations = []
    i = 0
    length = len(expression)
    while i < length:
        if expression[i].isdigit() or expression[i] == "!" or expression[i] == ".":
            token_list.append(expression[i])
            if expression[i] == "!":
                token_list.append(" ")
            i += 1
            continue
        if expression[i] == "-":
            if i == 0:
                stack_operations.append("neg")
                i += 1
                continue
            elif not expression[i - 1].isdigit():
                stack_operations.append("neg")
                i += 1
                continue
        if expression[i] == "(":
            stack_operations.append("(")
            token_list.append(" ")
            i += 1
            continue
        if expression[i] == ")":
            try:
                token_list.append(" ")
                finished = False
                while len(stack_operations) != 0 and not finished:
                    tmp = stack_operations.pop()
                    finished = tmp == "("
                    if not finished:
                        token_list.append(tmp)
                        token_list.append(" ")
                if not finished:
                    raise VerifyException("""ERROR: equilibrium of parentheses is violated.
                    Redundant closing parentheses found.""", i)
                else:
                    i += 1
            except VerifyException as error:
                return error.msg
            continue
        found = False
        for x in range(5, 0, -1):
            token = expression[i:i+x]
            if operations_to_stack[token] != -1:
                found = True
                if operations_to_stack[token] == 0:
                    stack_operations.append(token)
                else:
                    token_list.append(" ")
                    size = len(stack_operations)
                    if size != 0:
                        while operations_to_stack[stack_operations[size - 1]] != -1 and (
                              operations_to_stack[stack_operations[size - 1]] < operations_to_stack[token] or (
                               operations_to_stack[stack_operations[size - 1]] == operations_to_stack[token] and
                               token != "^")):
                            token_list.append(stack_operations.pop())
                            token_list.append(" ")
                            size -= 1
                            if size == 0:
                                break
                    stack_operations.append(token)
                i += x
                break
        if found:
            continue
        for x in operations_to_calculate:
            if expression[i:i+len(x)] == x:
                found = True
                result, shift, error_occurred = calculate_multiple_arguments_function(x, expression[i:])
                if error_occurred:
                    return "ERROR: something wrong in {0} function. Position - {1}.".format(x, i)
                i += shift
                token_list.append(str(result))
                token_list.append(" ")
                break
        if found:
            continue
        for x in constants:
            if expression[i:i+len(x)] == x:
                found = True
                token_list.append(x)
                token_list.append(" ")
                i += len(x)
                break
        if found:
            continue
        return "ERROR: Unknown symbol found. Position - {0}".format(i)
    token_list.append(" ")
    while len(stack_operations) != 0:
        tmp = stack_operations.pop()
        if tmp == "(":
            return """ERROR: equilibrium of parentheses is violated.
            Missing closing parentheses."""
        token_list.append(tmp)
        token_list.append(" ")
    reverse_expression = ''.join(token_list)
    print(reverse_expression)
    answer = calcexp.calculate_expression(reverse_expression)
    return answer


def calculate_multiple_arguments_function(func, args):
    """This is function to calculate round, pow functions immediately
       to spare us some headache at the next step: calculation of expression
    """
    exp_len = len(func)
    if args[exp_len] != "(":
        return 0, 0, True
    shift = args.find(")")
    numbers = args[exp_len + 1:shift].split(",")
    if len(numbers) > 3:
        return 0, 0, True
    shift += 1
    try:
        if len(numbers) == 3 and exp_len == 3:
            return pow(int(numbers[0]), int(numbers[1]), int(numbers[2])), shift, False
        elif len(numbers) == 2:
            if exp_len == 3:
                tmp_result = pow(float(numbers[0]), float(numbers[1]))
                if type(tmp_result) == complex:
                    return 0, 0, True
                else:
                    return tmp_result, shift, False
            if exp_len == 5:
                return round(float(numbers[0]), int(numbers[1])), shift, False
        else:
            return round(float(numbers[0])), shift, False
    except ValueError:
        return 0, 0, True
    except TypeError:
        return 0, 0, True
    return 0, 0, True
