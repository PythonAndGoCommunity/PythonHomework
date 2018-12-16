"""Operators, constants, unary operators and comparison symbol's for pycalc."""

import operator
import builtins
import math

from collections import namedtuple


UNARY_OPERATORS = {'-': '-@', '+': '+@'}


COMPARISON_SYMBOLS = ('!', '<', '>', '=')


OPERATOR = namedtuple('OPERATOR', 'priority function params_quantity')


OPERATORS = {
    '+': OPERATOR(1, operator.add, 2),
    '-': OPERATOR(1, operator.sub, 2),
    '*': OPERATOR(2, operator.mul, 2),
    '/': OPERATOR(2, operator.truediv, 2),
    '//': OPERATOR(2, operator.floordiv, 2),
    '%': OPERATOR(2, operator.mod, 2),
    '^': OPERATOR(3, operator.pow, 2),

    'sin': OPERATOR(4, math.sin, 1),
    'cos': OPERATOR(4, math.cos, 1),
    'asin': OPERATOR(4, math.asin, 1),
    'acos': OPERATOR(4, math.acos, 1),
    'sinh': OPERATOR(4, math.sinh, 1),
    'cosh': OPERATOR(4, math.cosh, 1),
    'asinh': OPERATOR(4, math.asinh, 1),
    'acosh': OPERATOR(4, math.acosh, 1),
    'tanh': OPERATOR(4, math.tanh, 1),
    'atanh': OPERATOR(4, math.atanh, 1),
    'tan': OPERATOR(4, math.tan, 1),
    'atan': OPERATOR(4, math.atan, 1),
    'hypot': OPERATOR(4, math.hypot, 3),
    'atan2': OPERATOR(4, math.atan2, 3),
    'exp': OPERATOR(4, math.exp, 1),
    'expm1': OPERATOR(4, math.expm1, 1),
    'log10': OPERATOR(4, math.log10, 1),
    'log2': OPERATOR(4, math.log2, 1),
    'log1p': OPERATOR(4, math.log1p, 1),
    'sqrt': OPERATOR(4, math.sqrt, 1),
    'abs': OPERATOR(4, builtins.abs, 1),
    'round': OPERATOR(4, builtins.round, 3),
    'log': OPERATOR(4, math.log, 3),

    '<': OPERATOR(0, operator.lt, 2),
    '<=': OPERATOR(0, operator.le, 2),
    '==': OPERATOR(0, operator.eq, 2),
    '!=': OPERATOR(0, operator.ne, 2),
    '>=': OPERATOR(0, operator.ge, 2),
    '>': OPERATOR(0, operator.gt, 2),
    ',': OPERATOR(0, None, 0),
    '(': OPERATOR(0, None, 0),
    ')': OPERATOR(5, None, 0),
    '-@': OPERATOR(2, None, 0),
    '+@': OPERATOR(2, None, 0)
}

CONSTANTS = {a: getattr(math, a) for a in dir(math) if isinstance(getattr(math, a), float)}
