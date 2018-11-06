"""This module contains lists and dictionaries of data that are used in other pycalc modules """

# general import
import math
import operator


# r_strings that are used to find operators / functions / etc
r_one_sign_operators = ['^\+', '^-', '^\*', '^/', '^\^', '^%']
r_two_signs_operators = ['^//', '^\*\*']
r_comparison_operators = ['^<=', '^>=', '^<', '^>', '^==', '^!=']
r_functions = ['^acosh', '^acos', '^asinh', '^asin', '^atan2', '^atanh', '^atan', '^ceil', '^copysign', '^cosh',
               '^cos', '^degrees', '^erfc', '^erf', '^expm1', '^exp', '^fabs', '^factorial', '^floor', '^fmod',
               '^gamma', '^gcd', '^hypot', '^isfinite', '^isinf', '^isnan', '^ldexp', '^lgamma', '^log10', '^log1p',
               '^log2', '^log', '^pow', '^radians', '^sinh', '^sin', '^sqrt', '^tanh', '^tan',  '^trunc',
               '^abs', '^round']
r_negative_functions = ['^-acosh', '^-acos', '^-asinh', '^-asin', '^-atan2', '^-atanh', '^-atan', '^-ceil',
                        '^-copysign', '^-cosh', '^-cos', '^-degrees', '^-erfc', '^-erf', '^-expm1', '^-exp',
                        '^-fabs', '^-factorial', '^-floor', '^-fmod', '^-gamma', '^-gcd', '^-hypot', '^-isfinite',
                        '^-isinf', '^-isnan', '^-ldexp', '^-lgamma', '^-log10', '^-log1p', '^-log2', '^-log',
                        '^-pow', '^-radians', '^-sinh', '^-sin', '-^sqrt', '^-tanh', '^-tan',  '^-trunc',
                        '^-abs', '^-round']
r_constants = ['^e', '^pi', '^tau', '^inf', '^nan']
r_negative_constants = ['^\-e', '^\-pi', '^\-tau', '^\-inf', '^\-nan']
r_int_numbers = ['^\d+']
r_negative_int_numbers = ['^\-\d+']
r_float_numbers = ['^\d+\.\d+|^\.\d+']
r_negative_float_numbers = ['^\-\d+\.\d+|^\-\.\d+']
r_brackets = ['^\(', '^\)']
r_comma = ['^,']
r_space = ['^\s']
# all r_strings together
r_strings = r_brackets + r_two_signs_operators + r_one_sign_operators + r_negative_functions + r_functions + \
            r_comparison_operators + r_negative_float_numbers + r_negative_int_numbers + r_negative_constants + \
            r_float_numbers + r_int_numbers + r_constants + r_space + r_comma  # the order matters


# acceptable constants and functions
constants = ['e', 'pi', 'tau', 'inf', 'nan']
negative_constants = ['-e', '-pi', '-tau', '-inf', '-nan']
functions = ['acosh', 'acos', 'asinh', 'asin', 'atan2', 'atanh', 'atan', 'ceil', 'copysign', 'cosh', 'cos',
             'degrees', 'erfc', 'erf', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum',
             'gamma', 'gcd', 'hypot', 'isclose', 'isfinite', 'isinf', 'isnan', 'ldexp', 'lgamma', 'log10',
             'log1p', 'log2', 'log', 'modf', 'pow', 'radians', 'sinh', 'sin', 'sqrt', 'tanh', 'tan', 'trunc',
             'round', 'abs']

negative_functions = ['-acosh', '-acos', '-asinh', '-asin', '-atan2', '-atanh', '-atan', '-ceil', '-copysign',
                      '-cosh', '-cos', '-degrees', '-erfc', '-erf', '-exp', '-expm1', '-fabs', '-factorial',
                      '-floor', '-fmod', '-frexp', '-fsum', '-gamma', '-gcd', '-hypot', '-isclose', '-isfinite',
                      '-isinf', '-isnan', '-ldexp', '-lgamma', '-log10', '-log1p', '-log2', '-log', '-modf',
                      '-pow', '-radians', '-sinh', '-sin', '-sqrt', '-tanh', '-tan', '-trunc', '-round', '-abs']


# acceptable operators
operators = ['+', '-', '*', '/', '//', '%', '^', '**']


# acceptable comparison operators
comparison_operators = ['<=', '>=', '<', '>', '==', '!=']


# operators precedence
precedence = {'(': 0, ')': 0, '<': 0, '>': 0, '<=': 0, '>=': 0, '==': 0, '!=': 0, '+': 1, '-': 1,
              '*': 2, '/': 2, '//': 2, '%': 2, '^': 3, '**': 3}


# numeric equivalents of constants
constants_numeric_equivalents = {'e': math.e, '-e': -math.e, 'pi': math.pi, '-pi': -math.pi, 'tau': math.tau,
                                 '-tau': -math.tau}


# operator's actions
operators_dict = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '^': operator.pow,
                  '**': operator.pow, '//': operator.floordiv, '%': operator.mod, '<': operator.lt, '>': operator.gt,
                  '<=': operator.le, '>=': operator.ge, '==': operator.eq, '!=': operator.ne}


# function's actions
# first element in a tuple associated with each key is a number of arguments for corresponding function
functions_dict = {'acos': (1, math.acos), 'acosh': (1, math.acosh), 'asin': (1, math.asin), 'asinh': (1, math.asinh),
                  'atan': (1, math.atan), 'atan2': (2, math.atan2), 'atanh': (1, math.atanh), 'ceil': (1, math.ceil),
                  'copysign': (2, math.copysign), 'cos': (1, math.cos), 'cosh': (1, math.cosh),
                  'degrees': (1, math.degrees), 'erf': (1, math.erf), 'erfc': (1, math.erfc), 'exp': (1, math.exp),
                  'expm1': (1, math.expm1), 'fabs': (1, math.fabs), 'factorial': (1, math. factorial),
                  'floor': (1, math.floor), 'fmod': (2, math.fmod), 'gamma': (1, math.gamma), 'gcd': (2, math.gcd),
                  'hypot': (2, math.hypot), 'isfinite': (1, math.isfinite), 'isinf': (1, math.isinf),
                  'isnan': (1, math.isnan), 'ldexp': (2, math.ldexp), 'lgamma': (1, math.lgamma), 'log': (2, math.log),
                  'log10': (1, math.log10), 'log1p': (1, math.log1p), 'log2': (1, math.log2), 'pow': (2, math.pow),
                  'radians': (1, math.radians), 'sin': (1, math.sin), 'sinh': (1, math.sinh), 'sqrt': (1, math.sqrt),
                  'tan': (1, math.tan), 'tanh': (1, math.tanh), 'trunc': (1, math.trunc), 'abs': (1, lambda x: abs(x)),
                  'round': (1, lambda x: round(x)), '-abs': (1, lambda x: -abs(x))}

if __name__ == '__main__':
    print('This module contains lists and dictionaries of data that are used in other pycalc modules')
