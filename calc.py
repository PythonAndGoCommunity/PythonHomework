import re
import math


class CalcError(Exception):
    pass


binary_operations = {
    "+": 0,
    "-": 0,
    "*": 1,
    "/": 1,
    "//": 1,
    "%": 1,
    "^": 2,
}

ops_list = {'abs', 'pow', 'round', 'log', 'log10', 'sqrt', 'sin', 'asin', 'cos', 'acos', 'hypot', 'tan', 'atan',
            'copysign', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'ldexp', 'fsum', 'isfinite', 'isinf',
            'isnan', 'modf', 'trunc', 'exp', 'expm1', 'log1p', 'log2', 'degrees', 'radians', 'cosh', 'sinh',
            'tanh', 'acosh', 'asinh', 'atanh', 'erf', 'erfc', 'gamma', 'lgamma', 'inv', 'gcd', 'isclose',
            'isdexp', 'atan2', 'ceil',
            }

constants = {
    "pi",
    "e",
    "tau",
    "inf",
    "nan",
}

comparison_operators = {
    "<",
    "<=",
    "==",
    "!=",
    ">=",
    ">",
}


def zeroless(expression):
    match = re.split(r'(?<=\W)(?=\.\d)', expression)
    return '0'.join(match)


def match_negative_value(expression):
    match = re.split(r'(?<=^-)(?=[a-z])|(?<=\(-)(?=[a-z])', expression)
    return '1'.join(match)


def insert_multiplication(expression):
    regex = r'(?<=\))(?=\w+)|(?<=\))(?=\()|(?<=[^a-z][^a-z]\d)(?=\()|(?<=^\d)(?=\()|(?<=\d)(?=e|[a-z][a-z])'
    match = re.split(regex, expression)
    return '*'.join(match)


def correct_expression(expression):
    expression = insert_multiplication(match_negative_value(zeroless(expression)))
    regex = r'(<=|==|!=|>=|log10|log2|log1p|expm1|atan2|^-\d+.\d+|^-\d+|(?<=\()-\d+.' \
            '\d+|(?<=\()-\d+|\//|\d+\.\d+|\d+|\W|\w+)'
    re_expr = re.split(regex, expression)
    re_expr = [x for x in re_expr if x and x != ' ']
    return re_expr


def get_arguments(expression):
    ops = expression.pop(0)
    res = []
    arg = []
    point = 1
    while expression:
        if expression[0] == ',':
            res.append(arg.copy())
            arg.clear()
        elif expression[0] == ')':
            point -= 1
            if point == 0:
                expression.remove(expression[0])
                res.append(arg)
                return ops, res
            else:
                arg.append(expression[0])
        elif expression[0] in ops_list:
            point += 1
            arg.append(expression[0])
        else:
            arg.append(expression[0])
        expression.remove(expression[0])


def is_float(val):
    try:
        float(val)
        return True
    except ValueError:
        return False


def calc(expression):
    stack = []
    while expression:
        i = expression[0]
        if is_float(i):
            stack.append(float(i))
            expression.remove(i)
        elif i in comparison_operators:
            operator = expression.pop(0)
            a = stack.pop()
            b = calc(expression)
            if operator == '<':
                res = a < b
            elif operator == '<=':
                res = a <= b
            elif operator == '==':
                res = a == b
            elif operator == '!=':
                res = a != b
            elif operator == '>=':
                res = a >= b
            elif operator == '>':
                res = a > b
            stack.append(res)
        elif i in constants:
            if i == "pi":
                stack.append(math.pi)
            elif i == "e":
                stack.append(math.e)
            elif i == "tau":
                stack.append(math.tau)
            elif i == "inf":
                stack.append(math.inf)
            elif i == "nan":
                stack.append(math.nan)
            expression.remove(i)
        elif i in binary_operations:
            if len(stack) > 1 and isinstance(stack[-1], (int, float)) and isinstance(stack[-2], (int, float)):
                b = stack.pop()
                a = stack.pop()
                if i == '+':
                    stack.append(a + b)
                elif i == '-':
                    stack.append(a - b)
                elif i == '*':
                    stack.append(a * b)
                elif i == '/':
                    stack.append(a / b)
                elif i == '//':
                    stack.append(a // b)
                elif i == '%':
                    stack.append(a % b)
                elif i == '^':
                    stack.append(a ** b)
            else:
                stack.append(i)
            expression.remove((i))
        if i in ops_list:
            arg = []
            ops, arg0 = get_arguments(expression)
            while arg0:
                arg.append(calc(arg0.pop()))
            if ops == 'pow':
                stack.append(pow(*arg))
            elif ops == 'abs':
                stack.append(abs(*arg))
            print(stack)
    print(stack)
    return stack.pop()


def to_postfix(expression):
    res = []
    stack = []
    ops_bracket = []
    for i in correct_expression(expression):
        if is_float(i) or i in ops_list or i in constants:
            res.append(i)
        elif i in comparison_operators:
            while stack:
                res.append(stack.pop())
            res.append(i)
        elif i == '(':
            if res and res[-1] in ops_list:
                ops_bracket.append(i)
            stack.append(i)
        elif i == ')':
            while stack[-1] != '(':
                res.append(stack.pop())
            stack.pop()
            if ops_bracket:
                ops_bracket.pop()
                res.append(i)
        elif i in binary_operations:
            if stack and stack[-1] in binary_operations and binary_operations[stack[-1]] >= binary_operations[i]:
                while stack and stack[-1] in binary_operations and binary_operations[stack[-1]] >= binary_operations[i]:
                    res.append(stack.pop())
                stack.append(i)
            else:
                stack.append(i)
        elif i == ',':
            while stack[-1] != '(':
                res.append(stack.pop())
            res.append(i)

    for i in reversed(stack):
        res.append(i)
    return res
