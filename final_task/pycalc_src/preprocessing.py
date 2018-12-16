"""Preprocessing module."""

from pycalc_src.exceptions import PreprocessingError

from pycalc_src.operators import OPERATORS
from pycalc_src.operators import CONSTANTS


def preprocessing(expression):
    """Prepare expression for calculate."""
    if not expression:
        raise PreprocessingError('expression is empty')

    if not isinstance(expression, str):
        raise PreprocessingError('expression is not a string')

    if expression.count('(') != expression.count(')'):
        raise PreprocessingError('brackets are not balanced')

    expression = expression.lower()

    #  if not _is_operators_available(expression):
        #  raise PreprocessingError('there are no operators in the expression')

    expression = expression.replace('**', '^')

    expression = _clean_repeatable_operators(expression)

    return expression


def _is_operators_available(expression):
    """Check operators in the expression."""
    for statement in OPERATORS:
        if statement in expression:
            return True

    for statement in CONSTANTS:
        if statement in expression:
            return True
    return False


def _clean_repeatable_operators(expression):
    """Delete from string repeatable operators."""
    repeatable_operators = {'+-': '-', '--': '+', '++': '+', '-+': '-'}

    while True:
        old_exp = expression
        for old, new in repeatable_operators.items():
            expression = expression.replace(old, new)
        if old_exp == expression:
            break

    return expression
