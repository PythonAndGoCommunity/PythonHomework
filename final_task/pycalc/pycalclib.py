"""This module contains a class that represents pycalclib and stores lists and dictionaries of data
that are used in other pycalc modules"""

# import
import math
import operator
import inspect
import sys


class Pycalclib:
    """A model of pycalclib"""

    def __init__(self, user_module):
        """Initialize pycalclib"""
        self.user_module = user_module
        # r_strings that are used to find operators / functions / etc
        self.r_one_sign_operators = [r'^\+', r'^-', r'^\*', r'^/', r'^\^', r'^%']
        self.r_two_signs_operators = [r'^//', r'^\*\*']
        self.r_comparison_operators = [r'^<=', r'^>=', r'^<', r'^>', r'^==', r'^!=']
        self.r_functions = [r'^acosh', r'^acos', r'^asinh', r'^asin', r'^atan2', r'^atanh', r'^atan', r'^ceil',
                            r'^copysign', r'^cosh', r'^cos', r'^degrees', r'^erfc', r'^erf', r'^expm1', r'^exp',
                            r'^fabs', r'^factorial', r'^floor', r'^fmod', r'^gamma', r'^gcd', r'^hypot', r'^isfinite',
                            r'^isinf', r'^isnan', r'^ldexp', r'^lgamma', r'^log10', r'^log1p', r'^log2', r'^log',
                            r'^pow', r'^radians', r'^sinh', r'^sin', r'^sqrt', r'^tanh', r'^tan',  r'^trunc',
                            r'^abs', r'^round']
        self.r_negative_functions = [r'^-acosh', r'^-acos', r'^-asinh', r'^-asin', r'^-atan2', r'^-atanh', r'^-atan',
                                     r'^-ceil', r'^-copysign', r'^-cosh', r'^-cos', r'^-degrees', r'^-erfc', r'^-erf',
                                     r'^-expm1', r'^-exp', r'^-fabs', r'^-factorial', r'^-floor', r'^-fmod',
                                     r'^-gamma', r'^-gcd', r'^-hypot', r'^-isfinite', r'^-isinf', r'^-isnan',
                                     r'^-ldexp', r'^-lgamma', r'^-log10', r'^-log1p', r'^-log2', r'^-log', r'^-pow',
                                     r'^-radians', r'^-sinh', r'^-sin', r'-^sqrt', r'^-tanh', r'^-tan',  r'^-trunc',
                                     r'^-abs', r'^-round']
        self.r_constants = [r'^e', r'^pi', r'^tau', r'^inf', r'^nan']
        self.r_negative_constants = [r'^\-e', r'^\-pi', r'^\-tau', r'^\-inf', r'^\-nan']
        self.r_int_numbers = [r'^\d+']
        self.r_negative_int_numbers = [r'^\-\d+']
        self.r_float_numbers = [r'^\d+\.\d+|^\.\d+']
        self.r_negative_float_numbers = [r'^\-\d+\.\d+|^\-\.\d+']
        self.r_brackets = [r'^\(', r'^\)']
        self.r_comma = [r'^,']
        self.r_space = [r'^\s']
        # acceptable constants and functions
        self.constants = ['e', 'pi', 'tau', 'inf', 'nan']
        self.negative_constants = ['-e', '-pi', '-tau', '-inf', '-nan']
        self.functions = ['acosh', 'acos', 'asinh', 'asin', 'atan2', 'atanh', 'atan', 'ceil', 'copysign', 'cosh',
                          'cos', 'degrees', 'erfc', 'erf', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod',
                          'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'isclose', 'isfinite', 'isinf', 'isnan', 'ldexp',
                          'lgamma', 'log10', 'log1p', 'log2', 'log', 'modf', 'pow', 'radians', 'sinh', 'sin', 'sqrt',
                          'tanh', 'tan', 'trunc', 'round', 'abs']
        self.negative_functions = ['-acosh', '-acos', '-asinh', '-asin', '-atan2', '-atanh', '-atan', '-ceil',
                                   '-copysign', '-cosh', '-cos', '-degrees', '-erfc', '-erf', '-exp', '-expm1',
                                   '-fabs', '-factorial', '-floor', '-fmod', '-frexp', '-fsum', '-gamma', '-gcd',
                                   '-hypot', '-isclose', '-isfinite', '-isinf', '-isnan', '-ldexp', '-lgamma',
                                   '-log10', '-log1p', '-log2', '-log', '-modf', '-pow', '-radians', '-sinh',
                                   '-sin', '-sqrt', '-tanh', '-tan', '-trunc', '-round', '-abs']
        # acceptable operators
        self.operators = ['+', '-', '*', '/', '//', '%', '^', '**']
        # acceptable comparison operators
        self.comparison_operators = ['<=', '>=', '<', '>', '==', '!=']
        # operators precedence
        self.precedence = {'(': 0, ')': 0, '<': 0, '>': 0, '<=': 0, '>=': 0, '==': 0, '!=': 0, '+': 1, '-': 1,
                           '*': 2, '/': 2, '//': 2, '%': 2, '^': 3, '**': 3}
        # numeric equivalents of constants
        self.constants_numeric_equivalents = {'e': math.e, '-e': -math.e, 'pi': math.pi, '-pi': -math.pi,
                                              'tau': math.tau, '-tau': -math.tau}
        # operators actions
        self.operators_dict = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv,
                               '^': operator.pow, '**': operator.pow, '//': operator.floordiv, '%': operator.mod,
                               '<': operator.lt, '>': operator.gt, '<=': operator.le, '>=': operator.ge,
                               '==': operator.eq, '!=': operator.ne}
        # functions actions
        # first element in a tuple associated with each key is a number of parameters for corresponding function
        self.functions_dict = {'acos': (1, math.acos), 'acosh': (1, math.acosh), 'asin': (1, math.asin),
                               'asinh': (1, math.asinh), 'atan': (1, math.atan), 'atan2': (2, math.atan2),
                               'atanh': (1, math.atanh), 'ceil': (1, math.ceil), 'copysign': (2, math.copysign),
                               'cos': (1, math.cos), 'cosh': (1, math.cosh), 'degrees': (1, math.degrees),
                               'erf': (1, math.erf), 'erfc': (1, math.erfc), 'exp': (1, math.exp),
                               'expm1': (1, math.expm1), 'fabs': (1, math.fabs), 'factorial': (1, math. factorial),
                               'floor': (1, math.floor), 'fmod': (2, math.fmod), 'gamma': (1, math.gamma),
                               'gcd': (2, math.gcd), 'hypot': (2, math.hypot), 'isfinite': (1, math.isfinite),
                               'isinf': (1, math.isinf), 'isnan': (1, math.isnan), 'ldexp': (2, math.ldexp),
                               'lgamma': (1, math.lgamma), 'log': (2, math.log), 'log10': (1, math.log10),
                               'log1p': (1, math.log1p), 'log2': (1, math.log2), 'pow': (2, math.pow),
                               'radians': (1, math.radians), 'sin': (1, math.sin), 'sinh': (1, math.sinh),
                               'sqrt': (1, math.sqrt), 'tan': (1, math.tan), 'tanh': (1, math.tanh),
                               'trunc': (1, math.trunc), 'abs': (1, lambda x: abs(x)),
                               'round': (1, lambda x: round(x)), '-abs': (1, lambda x: -abs(x))}

        if self.user_module != '':
            self.consider_user_module()

        self.r_strings = (self.r_brackets + self.r_two_signs_operators + self.r_one_sign_operators +
                          self.r_negative_functions + self.r_functions + self.r_comparison_operators +
                          self.r_negative_float_numbers + self.r_negative_int_numbers + self.r_negative_constants +
                          self.r_float_numbers + self.r_int_numbers + self.r_constants + self.r_space + self.r_comma)

    def consider_user_module(self):
        """Adds user functions into pycalclib"""
        try:
            user_module = __import__(self.user_module)
        except ModuleNotFoundError:
            print("ERROR: '{}' module hasn't been found".format(self.user_module))
            sys.exit(0)
        user_functions_info = inspect.getmembers(user_module, inspect.isfunction)
        # dictionary of user functions: key - func name string, value: (func_obj, func_num_params)
        user_functions = {}
        for item in user_functions_info:
            user_functions[item[0]] = (item[1], len(inspect.getfullargspec(item[1]).args))
        # add or replace functions in self.functions
        for func in user_functions.keys():
            if func not in self.functions:
                self.functions.insert(0, func)
                self.negative_functions.insert(0, ('-{}'.format(func)))
                self.r_functions.insert(0, (r'^{}'.format(func)))
                self.r_negative_functions.insert(0, (r'^-{}'.format(func)))
            self.functions_dict[func] = (user_functions[func][1], user_functions[func][0])
