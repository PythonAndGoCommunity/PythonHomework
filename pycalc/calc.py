#!/usr/bin/env python3
import re
import math
import argparse


class CalcError(Exception):
    """Calculation exception class"""
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


def fix_missing_zero(expression):
    """Inserts a zero in the number of the construction .number: .3 -> 0.3
    Args:
        expression: input string with math expression
    Returns:
        The return fixed string
    """
    match = re.split(r'(?<=\W)(?=\.\d)|(?<=^)(?=\.\d)', expression)
    return '0'.join(match)


def match_negative_value(expression):
    """Fix missing -1, if math function looks like -sin
    Args:
        expression: input string with math expression
    Returns:
        The return string with correct negative value
    """
    match = re.split(r'(?<=^-)(?=[a-z])|(?<=\(-)(?=[a-z])', expression)
    return '1'.join(match)


def insert_multiplication(expression):
    """Fix missing multiplication
    Args:
        expression: input string with math expression
    Returns:
        The return string with correct multiplication
    """
    regex = r'(?<=\))(?=\w+)|(?<=\))(?=\()|(?<=[^a-z][^a-z]\d)(?=\()|(?<=^\d)(?=\()|(?<=\d)(?=e|[a-z][a-z])'
    match = re.split(regex, expression)
    return '*'.join(match)


def correct_expression(expression):
    """Split expression by tokens
    Args:
        expression: input string with math expression
    Returns:
        The return list of tokens
    """
    if '()' in expression:
        raise CalcError('ERROR: invalid bracket expression')
    expression = insert_multiplication(match_negative_value(fix_missing_zero(expression)))
    regex = r'(<=|==|!=|>=|log10|log2|log1p|expm1|atan2|^-\d+.\d+|^-\d+|(?<=\()-\d+.' \
            '\d+|(?<=\()-\d+|\//|\d+\.\d+|\d+|\W|\w+)'
    re_expr = re.split(regex, expression)
    re_expr = [x for x in re_expr if x and x != ' ']
    return re_expr


def get_arguments(expression):
    """Get arguments for function
    Args:
        expression: input string start with math function
    Returns:
        The return list of arguments
    """
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


def is_float(value):
    """Check is value number
    Args:
        value: expression token
    Returns:
        The return True, if value is number and False if not
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def calc_iteration(expression):
    """Calculate math expression
    Args:
        expression: input string with math expression
    Returns:
        The return result of calculation
    """
    stack = []
    while expression:
        i = expression[0]
        if is_float(i):
            stack.append(float(i))
            expression.remove(i)
        elif i in comparison_operators:
            operator = expression.pop(0)
            a = stack.pop()
            b = calc_iteration(expression)
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
            stack.append(getattr(math, i))
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
                    try:
                        stack.append(a / b)
                    except ZeroDivisionError:
                        raise CalcError('ERROR: division by zero')
                elif i == '//':
                    try:
                        stack.append(a // b)
                    except ZeroDivisionError:
                        raise CalcError('ERROR: floor division by zero')
                elif i == '%':
                    try:
                        stack.append(a % b)
                    except ZeroDivisionError:
                        raise CalcError('ERROR: modulus by zero')
                elif i == '^':
                    stack.append(a ** b)
            else:
                stack.append(i)
            expression.remove((i))
        if i in ops_list:
            arg = []
            ops, arg0 = get_arguments(expression)
            while arg0:
                arg.append(calc_iteration(arg0.pop()))
            try:
                if ops == 'round':
                    stack.append(round(*arg))
                elif ops == 'abs':
                    stack.append(abs(*arg))
                else:
                    stack.append(getattr(math, ops)(*reversed(arg)))
            except ValueError:
                raise CalcError('ERROR: invalid argument for function {0}'.format(ops))
            except TypeError:
                raise CalcError('ERROR: invalid number of arguments for function {0}'.format(ops))
    return stack.pop()


def to_postfix(expression):
    """Convert infix notation to postfix notation
    Args:
        expression: input string with math expression
    Returns:
        The return expression in postfix notation
    """
    res = []
    stack = []
    ops_bracket = []
    expression = correct_expression(expression)
    if expression[0] in binary_operations:
        raise CalcError('ERROR: invalid operator "{0}"'.format(expression[0]))
    for item in range(len(expression)):
        i = expression[item]
        if is_float(i) or i in ops_list or i in constants:
            res.append(i)
        elif i in comparison_operators:
            while stack:
                res.append(stack.pop())
            res.append(i)
        elif i == '(':
            if expression[item + 1] in binary_operations:
                raise CalcError('ERROR: invalid operator "{0}"'.format(expression[item + 1]))
            if res and res[-1] in ops_list:
                ops_bracket.append(i)
            stack.append(i)
        elif i == ')':
            if '(' in stack:
                while stack[-1] != '(':
                    res.append(stack.pop())
            else:
                raise CalcError('ERROR: invalid bracket expression')
            stack.pop()
            if ops_bracket:
                ops_bracket.pop()
                res.append(i)
        elif i in binary_operations:
            if item + 1 >= len(expression) or expression[item + 1] in binary_operations:
                raise CalcError('ERROR: invalid operator "{0}"'.format(expression[:item + 1]))
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
        else:
            raise CalcError('ERROR: input invalid token "{0}"'.format(i))
    for i in reversed(stack):
        res.append(i)
    if '(' in res:
        raise CalcError('ERROR: invalid bracket expression')
    return res


def evaluate(expression):
    return calc_iteration(to_postfix(expression))


def main():
    """Calc main function"""
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument("EXPRESSION", help="expression string to evaluate")
    args = parser.parse_args()
    try:
        print(evaluate(args.EXPRESSION))
    except CalcError as exception:
        print(exception)


if __name__ == '__main__':
    main()
