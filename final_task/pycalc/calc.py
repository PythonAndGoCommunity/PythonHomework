#!/usr/bin/env python3
import re
import math
import argparse
import importlib


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

unary_operation = ['~']

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


def fix_multi_operations(expression):
    """Fix multiple operation with '+' and '-'
    Args:
        expression: input string with math expression
    Returns:
        The return fixed string
    """
    mul_operators = re.search(r'\+\+|\-\-|\+\-|-\+', expression)
    while mul_operators:
        expression = expression.replace('++', '+')
        expression = expression.replace('--', '+')
        expression = expression.replace('+-', '-')
        expression = expression.replace('-+', '-')
        mul_operators = re.search(r'\+\+|\-\-|\+\-|-\+', expression)
    return expression


def insert(regex, expression, token):
    """Inserts token in expression
    Args:
        regex: pattern to find position
        expression: input string with math expression
        token: token to insert
    Returns:
        The return fixed string
    """
    find = re.search(regex, expression)
    while find:
        position = re.search(regex, expression).end()
        expression = token.join([expression[:position], expression[position:]])
        find = re.search(regex, expression)
    return expression


def fix_missing_zero(expression):
    """Inserts a zero in the number of the construction .number: .3 => 0.3
    Args:
        expression: input string with math expression
    Returns:
        The return fixed string
    """
    token = '0'
    regex = r'(?<=\W)(?=\.\d)|(?<=^)(?=\.\d)'
    find = re.search(regex, expression)
    if not find:
        res = expression
    else:
        res = insert(regex, expression, token)
    return res


def match_negative_value(expression):
    """change unary minus to '~' for processing
    Args:
        expression: input string with math expression
    Returns:
        The return string with correct negative value
    """
    regex = re.compile(r'(?<=^-)(?=[a-z])|(?<=\(-)(?=[a-z])|(?<=\^\-)(?=[a-z])|(?<=\*\-)(?=[a-z])|'
                       r'(?<=\/\-)(?=[a-z])|(?<=\s\-)(?=[a-z])')
    find = re.search(regex, expression)
    if not find:
        res = expression
    else:
        while find:
            position = re.search(regex, expression).end()
            expression = '~'.join([expression[:position - 1], expression[position:]])
            find = re.search(regex, expression)
    return expression


def insert_multiplication(expression):
    """Fix missing multiplication
    Args:
        expression: input string with math expression
    Returns:
        The return string with correct multiplication
    """
    token = '*'
    regex = r'(?<=\))(?=\w+)|(?<=\))(?=\()|(?<=[^a-z][^a-z]\d)(?=\()|(?<=^\d)(?=\()|(?<=\d)(?=e|[a-z][a-z])'
    find = re.search(regex, expression)
    if not find:
        res = expression
    else:
        res = insert(regex, expression, token)
    return res


def correct_expression(expression):
    """Split expression by tokens
    Args:
        expression: input string with math expression
    Returns:
        The return list of tokens
    """
    res = []
    if expression == '':
        raise CalcError('ERROR: empty expression')
    expression = insert_multiplication(match_negative_value(fix_missing_zero(fix_multi_operations(expression))))
    regex = re.compile(r'(<=|==|!=|>=|(?<=[^a-z])e|e|pi|tau|inf|nan|log1p|^-\d+\.\d+|^-\d+|(?<=\W\W)\-\d+\.\d+|'
                       r'(?<=\W\W)\-\d+|(?<=\()\-\d+\.\d+|(?<=\()\-\d+|(?<=[a-z]\W)\-\d+\.\d+|(?<=[a-z]\W)\-\d+|'
                       r'(?<=\))\-|\//|\/|\d+\.\d+|\d+|\W|\w+)')
    re_expr = re.split(regex, expression)
    re_expr = [x for x in re_expr if x and x != ' ']
    for i in reversed(range(len(re_expr))):
        if i > 0:
            if re_expr[i] == '(' and is_float(re_expr[i - 1]):
                re_expr.insert(i, '*')
            elif re_expr[i] in constants and re_expr[i - 1] in constants:
                re_expr.insert(i, '*')
            elif (re_expr[i] in constants or re_expr[i] in ops_list) and is_float(re_expr[i - 1]):
                re_expr.insert(i, '*')
    return re_expr


def get_arguments(expression):
    """Get arguments for function
    Args:
        expression: input string start with math function
    Returns:
        The return list of arguments
    """
    ops = expression.pop(0)
    if not expression:
        raise CalcError('ERROR: invalid input')
    res = []
    arg = []
    point = 1
    while expression:
        if expression[0] == ',' and point == 1:
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


def is_func(value):
    """Check is value function
    Args:
        value: expression token
    Returns:
        The return True, if value is function and False if not
    """
    if value[0].isalpha or value[0] == '_':
        return True
    else:
        return False


def calc_iteration(expression, mod_list):
    """Calculate math expression
    Args:
        expression: input string with math expression
        mod_list: list of module names
    Returns:
        The return result of calculation
    """
    inv = 1
    stack = []
    while expression:
        i = expression[0]
        if is_float(i):
            stack.append(float(i))
            expression.remove(i)
        elif i in unary_operation:
            inv = -1
            expression.remove(i)
        elif i in comparison_operators:
            if len(expression) < 3:
                raise CalcError('ERROR: invalid input')
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
            stack.append(getattr(math, i) * inv)
            inv = 1
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
            expression.remove(i)
        else:
            arg = []
            ops, arg0 = get_arguments(expression)
            while arg0 and arg0 != [[]]:
                arg.append(calc_iteration(arg0.pop(0), mod_list))
            try:
                token = get_func(mod_list, ops)
                if token:
                    stack.append(token(*arg))
                elif ops == 'round':
                    stack.append(round(*arg) * inv)
                elif ops == 'abs':
                    stack.append(abs(*arg) * inv)
                else:
                    stack.append(getattr(math, ops)(*arg) * inv)
                inv = 1
            except ValueError:
                raise CalcError('ERROR: invalid argument for function {0}'.format(ops))
            except TypeError:
                raise CalcError('ERROR: invalid number of arguments for function {0}'.format(ops))
    if len(stack) > 1 or not is_float(stack[-1]):
        raise CalcError('ERROR: invalid expression')
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
        if i in comparison_operators:
            while stack:
                res.append(stack.pop())
            res.append(i)
        elif i == '(':
            if item + 1 >= len(expression) or expression[item + 1] in binary_operations:
                raise CalcError('ERROR: invalid operator')
            if res and is_func(res[-1]):
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
            if stack and stack[-1] in binary_operations and \
                    binary_operations[stack[-1]] >= binary_operations[i] and i != '^':
                while stack and stack[-1] in binary_operations and binary_operations[stack[-1]] >= binary_operations[i]:
                    res.append(stack.pop())
                stack.append(i)
            else:
                stack.append(i)
        elif i == ',':
            while stack[-1] != '(':
                res.append(stack.pop())
            res.append(i)
        elif is_float(i) or is_func(i) or i in unary_operation:
              res.append(i)
        else:
            raise CalcError('ERROR: input invalid token "{0}"'.format(i))
    for i in reversed(stack):
        res.append(i)
    if '(' in res:
        raise CalcError('ERROR: invalid bracket expression')
    return res


def evaluate(expression, mod_list):
    """Evaluate expression
    Args:
        expression: input string with math expression
        mod_list: list of module names
    Returns:
        The return result of evaluate
    """
    return calc_iteration(to_postfix(expression), mod_list)


def get_func(module_list, func_name):
    """Find function in imported module
    Args:
        module_list: list of modules to import
        func_name: function name
    Returns:
        The return function
    """
    for mod in module_list:
        imported = importlib.import_module(mod)
        if hasattr(imported, func_name):
            return getattr(imported, func_name)


def main():
    """Calc main function"""
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument("-m", "--use-modules", dest='MODULE', nargs='+',
                        required=False, default='', help="additional modules to use")
    parser.add_argument("EXPRESSION", help="expression string to evaluate")
    args = parser.parse_args()
    try:
        print(evaluate(args.EXPRESSION, args.MODULE))
    except CalcError as exception:
        print(exception)


if __name__ == '__main__':
    main()

