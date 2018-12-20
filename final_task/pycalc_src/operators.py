"""Operators, constants, unary operators and comparison symbol's for pycalc."""

import operator
import builtins
import math

from collections import namedtuple


UNARY_OPERATORS = {'-': '-@', '+': '+@'}


COMPARISON_SYMBOLS = ('!', '<', '>', '=')


OPERATOR = namedtuple('OPERATOR', 'priority function params_quantity have_brackets')


OPERATORS = {
    '+': OPERATOR(1, operator.add, 2, False),
    '-': OPERATOR(1, operator.sub, 2, False),
    '*': OPERATOR(2, operator.mul, 2, False),
    '/': OPERATOR(2, operator.truediv, 2, False),
    '//': OPERATOR(2, operator.floordiv, 2, False),
    '%': OPERATOR(2, operator.mod, 2, False),
    '^': OPERATOR(3, operator.pow, 2, False),
    'pow': OPERATOR(3, operator.pow, 3, True),

    'sin': OPERATOR(4, math.sin, 1, True),
    'cos': OPERATOR(4, math.cos, 1, True),
    'asin': OPERATOR(4, math.asin, 1, True),
    'acos': OPERATOR(4, math.acos, 1, True),
    'sinh': OPERATOR(4, math.sinh, 1, True),
    'cosh': OPERATOR(4, math.cosh, 1, True),
    'asinh': OPERATOR(4, math.asinh, 1, True),
    'acosh': OPERATOR(4, math.acosh, 1, True),
    'tanh': OPERATOR(4, math.tanh, 1, True),
    'atanh': OPERATOR(4, math.atanh, 1, True),
    'tan': OPERATOR(4, math.tan, 1, True),
    'atan': OPERATOR(4, math.atan, 1, True),
    'hypot': OPERATOR(4, math.hypot, 3, True),
    'atan2': OPERATOR(4, math.atan2, 3, True),
    'exp': OPERATOR(4, math.exp, 1, True),
    'expm1': OPERATOR(4, math.expm1, 1, True),
    'log10': OPERATOR(4, math.log10, 1, True),
    'log2': OPERATOR(4, math.log2, 1, True),
    'log1p': OPERATOR(4, math.log1p, 1, True),
    'sqrt': OPERATOR(4, math.sqrt, 1, True),
    'abs': OPERATOR(4, builtins.abs, 1, True),
    'round': OPERATOR(4, builtins.round, 3, True),
    'log': OPERATOR(4, math.log, 3, True),

    '<': OPERATOR(0, operator.lt, 2, False),
    '<=': OPERATOR(0, operator.le, 2, False),
    '==': OPERATOR(0, operator.eq, 2, False),
    '!=': OPERATOR(0, operator.ne, 2, False),
    '>=': OPERATOR(0, operator.ge, 2, False),
    '>': OPERATOR(0, operator.gt, 2, False),
    ',': OPERATOR(0, None, 0, False),
    '(': OPERATOR(0, None, 0, False),
    ')': OPERATOR(5, None, 0, False),
    '-@': OPERATOR(2, None, 0, False),
    '+@': OPERATOR(2, None, 0, False)
}

CONSTANTS = {a: getattr(math, a) for a in dir(math) if isinstance(getattr(math, a), float)}
