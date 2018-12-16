"""
This module allows to calculator functionality
"""

import math
import builtins
import os
import re
import sys
import operator as op
from .calculator_helper import PycalcError
from .calculator_helper import (
    check_is_number, check_may_unary_operator, check_is_unary_operator, check_right_associativity, check_is_callable,
    check_empty_expression, check_brackets_balance
)

PRIORITIES = {
    1: ['<', '>', '<=', '>=', '==', '!='],
    2: ['+', '-'],
    3: ['*', '/', '//', '%'],
    4: ['u+', 'u-'],
    5: ['^']
}

MODULES = [builtins, math]

BUILTINS_FUNCS = ['abs', 'round']

OPERATORS = {
    '+': op.add,
    '-': op.sub,
    'u-': -1,
    'u+': 1,
    '*': op.mul,
    '/': op.truediv,
    '//': op.floordiv,
    '%': op.mod,
    '^': op.pow,
    '<': op.lt,
    '>': op.gt,
    '<=': op.le,
    '>=': op.ge,
    '!=': op.ne,
    '==': op.eq
}


def import_modules(modules):
    """
    Import modules
    """
    sys.path.insert(0, os.path.abspath(os.path.curdir))
    for module in modules:
        try:
            import_module = __import__(module)
            MODULES.insert(0, import_module)
        except ModuleNotFoundError:
            raise PycalcError(f'Module "{module}" not found')


def split_operands(merged_operand):
    """
    Split operands
    :param merged_operand
    :return: list of operands
    """
    operands = []
    position = len(merged_operand)
    while merged_operand:
        if position < 0:
            raise PycalcError('Unexpected operand')
        current_string = merged_operand[:position]
        if get_module(current_string) or check_is_number(current_string):
            operands.append(current_string)
            merged_operand = merged_operand[position:]
            position = len(merged_operand)
        else:
            position -= 1
    return operands


def do_implicit_multiplication(expression):
    """
    Finds places where multiplication signs are missed and inserts them there
    :param expression
    :return: expression with multiply signs where they are missed
    """
    token_end_position = -1
    insert_positions = []
    expression = expression.replace(' ', '')
    expression = re.sub(r'\)\(', ')*(', expression)
    for i in range(len(expression)):
        if token_end_position >= i:
            continue
        j = i
        operand, token_end_position, i = find_operand(expression, i)
        if operand:
            operands = split_operands(operand)
            if not operands:
                raise PycalcError('Unexpected operand')
            elif len(operands) > 1:
                i = j
                splited_operands = '*'.join(operands)
                if i > 0 and expression[i - 1] == ')':
                    splited_operands = '*' + splited_operands
                expression = expression.replace(operand, splited_operands)
                token_end_position = i + len('*'.join(operands[:-1]))
                operand = operands[-1]
        module = get_module(operand)
        is_call = False
        if module:
            is_call = check_is_callable(operand, module)
        if operand and check_is_number(operand) or module:
            j = i - len(operand) - 1
            if j > 0:
                if j and j != i and expression[j] == ')':
                    insert_positions.append(j + 1 + len(insert_positions))
            j = i
            if j < len(expression) and expression[j] == '(' and not is_call:
                insert_positions.append(j + len(insert_positions))
    expression = list(expression)
    for i in insert_positions:
        expression.insert(i, '*')
    return ''.join(expression)


def check_may_valid_operation(last_operator, current_operator):
    """
    :param last_operator
    :param current_operator
    :return: True if operation is valid
    """
    if check_is_unary_operator(current_operator) and get_priority(current_operator) < get_priority(last_operator):
        return
    return True


def get_module(attribute):
    """
    :return: module that contains the attribute
    """
    for module in MODULES:
        if hasattr(module, attribute):
            if module == builtins and attribute not in BUILTINS_FUNCS:
                continue
            return module
    return


def split_arguments(arguments_string):
    """
    Get function arguments from string
    :param arguments_string
    :return: arguments
    """
    brackets = {'(': 1, ')': -1}
    count = 0
    split_positions = []
    arguments = []
    for i, symbol in enumerate(arguments_string):
        if symbol in brackets:
            count += brackets[symbol]
        elif symbol == ',' and not count:
            split_positions.append(i)

    for i, position in enumerate(split_positions):
        if i == 0:
            arguments.append(arguments_string[:position])
        elif i < len(split_positions):
            arguments.append(arguments_string[split_positions[i - 1] + 1:position])

    if split_positions:
        arguments.append(arguments_string[split_positions[-1] + 1:])
    elif not arguments:
        arguments.append(arguments_string)
    return arguments


def process_func_or_const(operand, expression, token_end_position, module):
    """
    :param operand
    :param expression
    :param token_end_position
    :param module
    :return: the constant or result of the function and
    position of the last symbol if this is function
    """
    if callable(getattr(module, operand)):
        count = 0
        inner_expression = ''
        brackets = {'(': 1, ')': -1}
        if token_end_position < len(expression) and expression[token_end_position] == '(':
            count += 1
            token_end_position += 1
            while count:
                if expression[token_end_position] in brackets:
                    count += brackets[expression[token_end_position]]
                if not count:
                    break
                inner_expression += expression[token_end_position]
                token_end_position += 1
        args = ()
        if inner_expression:
            raw_arguments = split_arguments(inner_expression)
            if not raw_arguments[-1]:
                raw_arguments.pop()
            args = [calculate(arg) for arg in raw_arguments]
        try:
            func_result = getattr(module, operand)(*args)
            if not check_is_number(func_result):
                raise PycalcError('Unsupported function result')
            return func_result, token_end_position
        except (TypeError, ValueError) as error:
            raise PycalcError(error)

    return getattr(module, operand), None


def get_priority(operator):
    """
    :param operator
    :return: priority of operator
    """
    for priority, operators in PRIORITIES.items():
        if operator in operators:
            return priority
    return -1


def check_comparison_priority(operators):
    """
    :param operators
    :return: True if the list of operators is only comparison operators
    False otherwise
    """
    for operator in operators:
        if get_priority(operator) > 1:
            return
    return True


def check_valid_spaces(expression):
    """
    Check spaces for validity
    :param expression
    """
    is_last_number, is_last_operator, is_space = False, False, False
    token_end_position = -1
    for i, symbol in enumerate(expression):
        if symbol in ['(', ')']:
            is_last_number, is_last_operator, is_space = False, False, False
        elif token_end_position >= i:
            continue
        elif symbol == ' ':
            is_space = True
        elif symbol in OPERATORS or (i < len(expression) - 1 and symbol + expression[i + 1] in OPERATORS):
            if is_last_operator and is_space and not check_may_unary_operator(symbol):
                raise PycalcError('Missed operand')
            else:
                token_end_position = i + get_length_operator(expression, i) - 1
            is_last_number, is_last_operator, is_space = False, True, False
        else:
            if symbol in ['!', '=']:
                raise PycalcError('Invalid operator')
            is_last_operator, is_space = False, False
            operand, token_end_position, i = find_operand(expression, i)
            if check_is_number(operand):
                if is_last_number:
                    raise PycalcError('Missed operator')
                is_last_number = True
            else:
                is_last_number = False


def execute_comparison(operands, operators):
    """
    :param operands
    :param operators
    :return: False if at least one comparison return False
    True otherwise
    """
    if len(operands) == len(operators) + 1:
        for i, operator in enumerate(operators):
            if not OPERATORS[operator](operands[i], operands[i + 1]):
                return False
        return True
    raise PycalcError('Missed operator or operand')


def execute_operation(operands, operator):
    """
    Execute operation with operands and put result into list of the operands
    :param operands
    :param operator
    """
    if operands:
        right = operands.pop()
        if operator.startswith('u'):
            operands.append(OPERATORS[operator] * right)
        elif operands:
            left = operands.pop()
            operands.append(OPERATORS[operator](left, right))
        else:
            raise PycalcError('Missed operator or operand')


def do_final_execution(operators, operands):
    """
    Execute operations with operands while list of operators not empty
    :param operators
    :param operands
    :return: result of calculation
    """
    if not operands:
        raise PycalcError('Missed operator')
    while operators:
        if not check_comparison_priority(operators):
            execute_operation(operands, operators.pop())
        else:
            operands = [execute_comparison(operands, operators)]
            break

    if isinstance(operands[-1], complex):
        raise PycalcError('Negative number cannot be raised to a fractional power')

    elif len(operands) > 1:
        raise PycalcError('Missed operator')

    answer = operands.pop()
    if answer % 1 or isinstance(answer, bool):
        return answer
    return int(answer)


def find_operand(expression, position):
    """
    :param expression
    :param position
    :return: operand, position of the last symbol of the operand,
    position of symbol after operand
    """
    operand = ''
    while position < len(expression) and (expression[position].isalnum() or expression[position] == '.'):
        operand += expression[position]
        position += 1
    token_end_position = position - 1

    return operand, token_end_position, position


def get_length_operator(expression, position):
    """
    :param expression
    :param position
    :return: length of operator
    """
    if position < len(expression) - 1 and expression[position] + expression[position + 1] in OPERATORS:
        return 2
    return 1


def validate_expression(expression):
    """
    Validate expression
    :param expression
    """
    check_empty_expression(expression)
    check_brackets_balance(expression)
    check_valid_spaces(expression)


def update_operands(expression, operands, index):
    """
    :param expression
    :param operands
    :param index: index of symbol with which the operand starts
    :return: token's end position index
    """
    operand, token_end_position, index = find_operand(expression, index)

    module = get_module(operand)
    if check_is_number(operand):
        operand = float(operand)
        if not operand % 1:
            operand = int(operand)
        operands.append(operand)
    elif module:
        new_operand, tmp_token_end_position = process_func_or_const(operand, expression, index, module)
        operands.append(new_operand)
        if tmp_token_end_position:
            token_end_position = tmp_token_end_position
    else:
        raise PycalcError('Unexpected operand')

    return token_end_position


def update_operators(expression, operator, operators, operands, is_unary, token_end_position, index):
    """
    :param expression
    :param operator
    :param operators
    :param operands
    :param is_unary
    :param token_end_position
    :param index: index of symbol with which the operator starts
    :return: token's end position index
    """
    if not is_unary and index:
        prev_symbol = expression[index - 1]
        if prev_symbol in OPERATORS:
            is_unary = True

    if index < len(expression) - 1 and operator + expression[index + 1] in OPERATORS:
        operator += expression[index + 1]
        token_end_position = index + 1

    if is_unary and check_may_unary_operator(operator):
        operator = 'u' + operator

    if get_priority(operator) >= 1 or (is_unary and check_may_unary_operator(operator)):
        while operators and operands:
            condition_a = not check_right_associativity(operator)
            condition_b = get_priority(operators[-1]) >= get_priority(operator)
            condition_c = check_right_associativity(operator)
            condition_d = get_priority(operators[-1]) > get_priority(operator)
            condition = condition_a and condition_b or condition_c and condition_d

            if check_may_valid_operation(operators[-1], operator) and get_priority(operators[-1]) > 1 and condition:
                execute_operation(operands, operators.pop())
            else:
                break
    operators.append(operator)
    return token_end_position


def calculate(expression):
    """
    :param expression
    :return: result of calculation
    """
    check_empty_expression(expression)
    operands = []
    operators = []
    token_end_position = -1
    is_unary = True
    for index, symbol in enumerate(expression):
        if token_end_position >= index:
            continue
        elif symbol == '(':
            operators.append(symbol)
            is_unary = True
        elif symbol == ')':
            while operators[-1] != '(':
                execute_operation(operands, operators.pop())
            operators.pop()
            is_unary = False
        elif symbol in OPERATORS or (index < len(expression) - 1 and symbol + expression[index + 1] in OPERATORS):
            token_end_position = update_operators(expression, symbol, operators, operands,
                                                  is_unary, token_end_position, index)
        else:
            token_end_position = update_operands(expression, operands, index)
            is_unary = False

    return do_final_execution(operators, operands)


def do_calculation(expression, modules=None):
    """
    Import user modules and calculate expression
    :param expression
    :param modules
    :return: result of calculation
    """
    try:
        if modules:
            import_modules(modules)

        validate_expression(expression)
        expression = do_implicit_multiplication(expression)
        return calculate(expression)

    except PycalcError as error:
        return error
