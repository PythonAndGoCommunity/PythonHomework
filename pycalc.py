import argparse
import re
import math

operators = {'+': (1, lambda x, y: x + y),
             '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y),
             '/': (2, lambda x, y: x / y),
             '//': (2, lambda x, y: x // y),
             '%': (2, lambda x, y: x % y),
             '^': (4, lambda x, y: x ** y),
             'atan2': (3, lambda x, y: math.atan2(x, y)),
             'copysign': (3, lambda x, y: math.copysign(x, y)),
             'fmod': (3, lambda x, y: math.fmod(x, y)),
             'gcd': (3, lambda x, y: math.gcd(x, y)),
             'hypot': (3, lambda x, y: math.hypot(x, y)),
             'isclose': (3, lambda x, y: math.isclose(x, y)),
             'ldexp': (3, lambda x, y: math.ldexp(x, y)),
             'pow': (3, lambda x, y: math.pow(x, y)),
             'log': (3, lambda x, y: math.log(x, y)),
             'acos': (3, lambda x: math.acos(x)),
             'acosh': (3, lambda x: math.acosh(x)),
             'asin': (3, lambda x: math.asin(x)),
             'asinh': (3, lambda x: math.asinh(x)),
             'atan': (3, lambda x: math.atan(x)),
             'atanh': (3, lambda x: math.atanh(x)),
             'ceil': (3, lambda x: math.ceil(x)),
             'cos': (3, lambda x: math.cos(x)),
             'cosh': (3, lambda x: math.cosh(x)),
             'degrees': (3, lambda x: math.degrees(x)),
             'erf': (3, lambda x: math.erf(x)),
             'erfc': (3, lambda x: math.erfc(x)),
             'exp': (3, lambda x: math.exp(x)),
             'expm1': (3, lambda x: math.expm1(x)),
             'fabs': (3, lambda x: math.fabs(x)),
             'factorial': (3, lambda x: math.factorial(x)),
             'floor': (3, lambda x: math.floor(x)),
             'frexp': (3, lambda x: math.frexp(x)),
             'gamma': (3, lambda x: math.gamma(x)),
             'isfinite': (3, lambda x: math.isfinite(x)),
             'isinf': (3, lambda x: math.isinf(x)),
             'isnan': (3, lambda x: math.isnan(x)),
             'lgamma': (3, lambda x: math.lgamma(x)),
             'log10': (3, lambda x: math.log10(x)),
             'log1p': (3, lambda x: math.log1p(x)),
             'log2': (3, lambda x: math.log2(x)),
             'modf': (3, lambda x: math.modf(x)),
             'radians': (3, lambda x: math.radians(x)),
             'sin': (3, lambda x: math.sin(x)),
             'sinh': (3, lambda x: math.sinh(x)),
             'sqrt': (3, lambda x: math.sqrt(x)),
             'tan': (3, lambda x: math.tan(x)),
             'tanh': (3, lambda x: math.tanh(x)),
             'trunc': (3, lambda x: math.trunc(x)),
             'round': (3, lambda x: round(x)),
             'abs': (3, lambda x: abs(x))
             }

const = {'pi': math.pi,
            'e': math.e,
            'inf': math.inf,
            'nan': math.nan,
            'tau': math.tau
         }

# two value operators
doubleOperators = ['+', '-', '*', '/', '%', '^', '//', '%', 'atan2', 'copysign', 'fmod', 'gcd', 'hypot', 'isclose',
                    'ldexp', 'pow', 'log']



# the list of operators
operList = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign', 'cos', 'cosh',
                  'degrees', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum',
                  'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf', 'isnan', 'ldexp', 'lgamma', 'log',
                  'log10', 'log1p', 'log2', 'modf', 'nan', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh',
                  'tau', 'trunc', 'round', 'abs', '+', '-', '*', '/', '%', '^', '//', '(', ')', 'e', 'pi', 'inf',
            'nan', 'tau']



compareOperators = {'==': (lambda x, y: x == y),
                     '>=': (lambda x, y: x >= y),
                     '<=': (lambda x, y: x <= y),
                     '!=': (lambda x, y: x != y),
                     '<': (lambda x, y: x < y),
                     '>': (lambda x, y: x > y)
                    }



def main():


    parser = argparse.ArgumentParser()
    parser.add_argument("EXPRESSION", help="expression string to evaluate", type=str)
    args = parser.parse_args()

    # start main count with parsed arguments
    print(main_count(args.EXPRESSION))


if __name__ == '__main__':
    print(main_count('fsum([9])'))
