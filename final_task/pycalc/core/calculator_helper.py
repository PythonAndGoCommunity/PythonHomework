"""
This module contains auxiliary functions for the calculator
"""


class PycalcError(Exception):
    def __init__(self, message):
        super().__init__('ERROR: ' + str(message))


def is_number(string):
    """
    :return: True if the string is a number
    False otherwise
    """
    try:
        float(string)
        return True
    except ValueError:
        return


def may_unary_operator(operator):
    """
    :return: True if the operator may be unary
    False otherwise
    """
    return operator in ['+', '-']


def is_unary_operator(operator):
    """
    :return: True if the operator is unary
    False otherwise
    """
    return operator in ['u+', 'u-']


def check_right_associativity(operator):
    """
    :return: True if the operator is ^
    False otherwise
    """
    return operator == '^'


def is_callable(attribute, module):
    """
    :return: True if the attribute is callable
    False otherwise
    """
    return callable(getattr(module, attribute))


def check_brackets_balance(expression):
    """
    :return: True if the brackets are balanced
    False otherwise
    """
    brackets = {'(': 1, ')': -1}
    count = 0
    for symbol in expression:
        if symbol in brackets:
            count += brackets[symbol]
        if count < 0:
            raise PycalcError('Brackets are not balanced')
    if count:
        raise PycalcError('Brackets are not balanced')


def check_empty_expression(expression):
    """
    :raise exception if expression is empty
    """
    if not expression:
        raise PycalcError('Empty expression while execute')
