#!/usr/bin/env python3

import argparse
import math
import re

# dict { name function: (execution priority, calculation)}
OPERATORS = {'+': (1, lambda x, y: x + y),
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

constant = {'pi': math.pi,
            'e': math.e,
            'inf': math.inf,
            'nan': math.nan,
            'tau': math.tau
            }

# all operators
OPERATORS_func = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign', 'cos', 'cosh',
                  'degrees', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum',
                  'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf', 'isnan', 'ldexp', 'lgamma', 'log',
                  'log10', 'log1p', 'log2', 'modf', 'nan', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh',
                  'tau', 'trunc', 'round', 'abs', '+', '-', '*', '/', '%', '^', '//', '(', ')', 'e', 'pi', 'inf',
                  'nan', 'tau']

# operators that take two values
OPERATORS_double = ['+', '-', '*', '/', '%', '^', '//', '%', 'atan2', 'copysign', 'fmod', 'gcd', 'hypot', 'isclose',
                    'ldexp', 'pow', 'log']

OPERATORS_compare = {'==': (lambda x, y: x == y),
                     '>=': (lambda x, y: x >= y),
                     '<=': (lambda x, y: x <= y),
                     '!=': (lambda x, y: x != y),
                     '<': (lambda x, y: x < y),
                     '>': (lambda x, y: x > y)
                     }


def main_count(formula):
    """Main function

    Pure command-line calculator using python.
    Formula must include string positional arguments:
    "EXPRESSION  expression string to evaluate".

    """

    def check_error(formula):
        """Check error function

        Validation check

        """

        if not formula:
            return "ERROR: no value"
        else:

            if formula[-1] in OPERATORS:
                return "ERROR: syntax mistake"
            if formula[0] in '^%*/= |\\':
                return "ERROR: syntax mistake"

            if re.search(r'\d\s\d', formula):
                return "ERROR: syntax mistake"

            if formula.count('(') != formula.count(')'):
                return "ERROR: brackets are not balanced"

            if formula in OPERATORS:
                return "ERROR: no function arguments"

            if '()' in formula or '[]' in formula:
                return "ERROR: no function arguments"

            if re.search(r'[*,/,<,>,%,^][*,/,<,>,%,^]', formula):
                return "ERROR: syntax error in statements"

            if re.search(r'[*,/,<,>,%,^,=]\s[*,/,<,>,%,^,=]', formula):
                return "ERROR: syntax error in statements"

            if re.search(r'log[1,2][0,p][^(]', formula):
                return "ERROR: unknown function"

            # function argument checking
            for name_func in OPERATORS:
                if name_func.isalpha() or name_func in ['log1p', 'log10', 'atan2', 'expm1', 'log2']:
                    # split by function name + '('
                    name_func_bracket = '{}('.format(name_func)

                    if name_func_bracket in formula:

                        for expression in formula.split(name_func_bracket)[1:]:
                            count_brackets = 0
                            count_arguments = 0
                            for key in expression:
                                if key == ',' and not count_brackets:
                                    # arguments are separated by commas
                                    # count when no count_brackets
                                    count_arguments += 1

                                if key == ')' and not count_brackets:
                                    break
                                elif key == ')':
                                    count_brackets -= 1
                                elif key == '(':
                                    count_brackets += 1

                            if count_arguments > 1:
                                return "ERROR: function arguments are not balanced"
                            # function pow has two or one argument
                            elif (count_arguments > 1 or count_arguments == 0) and name_func == 'pow':
                                return "ERROR: function arguments are not balanced"
                            # these functions have 2 arguments
                            elif count_arguments == 0 and name_func in ['atan2', 'copysign', 'fmod', 'gcd', 'hypot',
                                                                        'isclose', 'ldexp', 'pow']:
                                return "ERROR: function arguments are not balanced"
                            # other functions with 1 argument
                            elif count_arguments > 0 and name_func not in ['atan2', 'copysign', 'fmod', 'gcd', 'hypot',
                                                                           'isclose', 'ldexp', 'pow', 'log']:
                                return "ERROR: function arguments are not balanced"

    def function_format_two_arguments(formula, name_function):
        """ Formatting formula with two arguments """

        result_formula = formula
        first_argument = []
        second_argument = []
        count_argument = True
        count_bracket = 0

        # find first and second argument
        for key in (name_function).join(formula.split('{}'.format(name_function))[1:]):

            if key == '(':
                count_bracket += 1
            if key == ')':
                count_bracket -= 1
            if key == ',':
                first_argument.pop(0)
                count_argument = False

            if key == ')' and not count_bracket and not count_argument:
                break
            elif key == ')' and not count_bracket:
                first_argument.append(key)
                break

            elif count_argument:
                first_argument.append(key)

            else:
                if key != ',':
                    second_argument.append(key)

        # if not second argument into log - the base by log = e
        # if log(x) format into log(x,e)
        if not second_argument and name_function == 'log':
            second_argument.append('e')
            replace_expression = "{}{}".format(name_function, ''.join(first_argument), 1)
        else:
            replace_expression = "{}({},{})".format(name_function, ''.join(first_argument),
                                                    ''.join(second_argument), 1)

        # count every argument
        x = main_count(''.join(first_argument))
        y = main_count(''.join(second_argument))

        # function gcd have only int arguments
        if name_function == 'gcd':
            x = int(x)
            y = int(y)

        result_function = OPERATORS[name_function][1](x, y)
        # replace only 1 time
        result_formula = result_formula.replace(replace_expression, str(result_function), 1)

        # double entry check
        if name_function == 'log':
            # there are log2p, log10 with 1 argument
            if 'log(' in result_formula:
                result_formula = function_format_two_arguments(result_formula, name_function)
        else:
            if name_function in result_formula:
                result_formula = function_format_two_arguments(result_formula, name_function)

        return result_formula

    def format_degree_priority(formula):
        """Function add priority degree

        If we have more than one degree - then add next degree with high priority.
        """

        result_formula = []

        for i, key in enumerate(formula.split('^')):
            result_formula.append(key)
            if i != len(formula.split('^')) - 1:
                result_formula.append('^' * (i + 1))
                # add in OPERATORS degree with high priority
                OPERATORS.update({'^' * (i + 1): (4 + i, lambda x, y: x ** y)})
                OPERATORS_double.append('^' * (i + 1))
                OPERATORS_func.append('^' * (i + 1))

        return ''.join(result_formula)

    def function_format_degree_replace_function(formula):
        """Function replace degree by function into degree by function with brackets

        For example: 1^sin(pi) into ==> 1^(sin(pi))
        """

        expression = []
        count_argument = False
        count_bracket = 0
        for i, key in enumerate(formula):

            if key == '(':
                count_bracket += 1
            elif key == ')':
                count_bracket -= 1

            if count_argument:
                expression.append(key)

            if key == ')' and not count_bracket and count_argument:
                break

            if key == '^' and formula[i + 1].isalpha():
                count_argument = True
        # replace only 1 time
        formula = formula.replace("{}".format(''.join(expression)), "({})".format(''.join(expression)), 1)

        # replace other instance
        count = False
        for i, key in enumerate(formula):
            if key == '^' and formula[i + 1].isalpha():
                count = True
                break
        if count:
            formula = function_format_degree_replace_function(formula)

        return formula

    def replace_degree_negative_number(formula):
        """Function replace negative number with degree in formula into zero with brackets

        For example:
            replace  ^-5 ==> into ^(0-5)
            ^-e == > into ^(0-e)
            ^-cos() == > into ^(0-cos())
            ^-(1+2) == > into ^(0-(1+2))

        """

        expression = []
        count = False
        bracket_count = 0
        for i, key in enumerate(formula):

            if count:
                if key == ')' and not bracket_count:
                    expression.append(key)
                    break
                elif key == ')':
                    bracket_count -= 1
                elif key == '(':
                    bracket_count += 1

                if expression and (key in OPERATORS_double or key in OPERATORS_compare) and not bracket_count:
                    break
                else:
                    expression.append(key)

            if key == '^' and formula[i + 1] == '-':
                count = True

        # replace only first expression
        formula = formula.replace(("^{}".format(''.join(expression))), "^(0{})".format(''.join(expression)), 1)

        # replace other expressions
        if '^-' in formula:
            formula = replace_degree_negative_number(formula)

        return formula

    def format_function_fsum(formula):
        """Format function fsum
        Calculate this function here because fsum has many arguments

        replace fsum([1,2]) ==> into 3

        """

        count_brackets = 0
        count_brackets_square = 0
        count_arguments = []
        add_argument = []

        for key in formula.split('fsum([', 1)[1:][0]:
            if key == "]" and not count_brackets_square:
                break

            if key == ',' and not count_brackets:
                count_arguments.append(''.join(add_argument))
                add_argument = []
            else:
                add_argument.append(key)

            if key == ']':
                count_brackets_square -= 1
            elif key == '[':
                count_brackets_square += 1
            elif key == ')':
                count_brackets -= 1
            elif key == '(':
                count_brackets += 1

        count_arguments.append(''.join(add_argument))

        result_count = 0
        for argument in count_arguments:
            result_count += float(main_count(argument))

        replace_expression = "fsum([{}])".format(','.join(count_arguments), 1)

        result_formula = formula.replace(replace_expression, str(result_count), 1)

        return result_formula

    def formula_formatting(formula):
        """Formula formatting

        Getting the formula to a readable form for reverse Polish notation.

        """

        # delete backspace
        formula = formula.replace(' ', '')
        # replace )( into )*( for readable form
        formula = formula.replace(')(', ')*(')
        # replace (- into (0- for readable form
        formula = '(0-'.join(formula.split('(-'))

        # formatting a formula with two arguments
        for name_function in ['pow', 'log(', 'copysign', 'ldexp', 'atan2', 'hypot', 'fmod', 'gcd']:
            if name_function in formula:
                # use only log (without log10,log1p)
                if name_function == 'log(':
                    name_function = 'log'
                formula = function_format_two_arguments(formula, name_function)

        # find degree by function
        for i, key in enumerate(formula):
            if key == '^' and formula[i + 1].isalpha():
                formula = function_format_degree_replace_function(formula)
                break

        # find the number of degrees
        if formula.count("^") > 1:
            formula = format_degree_priority(formula)

        # replace sign "+","-" in front formula
        new_data = []
        new_data.append(formula[0])

        for token in formula[1:]:
            if new_data[-1] == '+' and token == '-':
                new_data[-1] = '-'
            elif new_data[-1] == '-' and token == '+':
                new_data[-1] = '-'
            elif new_data[-1] == '-' and token == '-':
                new_data[-1] = '+'
            elif new_data[-1] == '+' and token == '+':
                new_data[-1] = '+'
            else:
                new_data.append(token)
        if new_data[0] == '-':
            new_data.insert(0, '0')
        if new_data[0] == '+':
            new_data.pop(0)

        formula = ''.join(new_data)

        # replace negative number in formula into zero with brackets
        # replace 5/-1 into 5*(0-1)/1
        formula = formula.replace('/-', '*(0-1)/')
        formula = formula.replace('*-', '*(0-1)*')

        # replace negative number with degree in formula into zero with brackets
        if '^-' in formula:
            formula = replace_degree_negative_number(formula)

        # format function fsum because fsum([1,2,3,4..]) has many arguments
        if 'fsum' in formula:
            formula = format_function_fsum(formula)

        return formula

    def split_formula(formatted_formula):
        """Function splitting formula into keys

        Return iterator.

        """

        stack = []
        for i, key in enumerate(formatted_formula):

            if key in '1234567890.':
                # check log10 log1p log2
                if len(stack) > 2 and ''.join(stack[:3]) == 'log':

                    stack.append(key)
                    if ''.join(stack) in OPERATORS_func:
                        yield ''.join(stack)
                        stack = []

                elif stack and (stack[0] not in '1234567890.'):
                    yield ''.join(stack)
                    stack = []
                    stack.append(key)
                else:
                    stack.append(key)

            else:
                if key in '()':
                    if stack and (stack[0] in '1234567890.'):
                        yield float(''.join(stack))
                    elif stack:
                        yield ''.join(stack)

                    stack = []
                    stack.append(key)

                elif len(stack) > 2 and ''.join(stack[:3]) == 'log':
                    stack.append(key)
                    if ''.join(stack) in OPERATORS_func:
                        yield ''.join(stack)
                        stack = []

                elif stack and stack[0] in '1234567890.':
                    yield float(''.join(stack))
                    stack = []
                    stack.append(key)

                else:

                    if ''.join(stack) + key in OPERATORS_func:
                        stack.append(key)

                    elif ''.join(stack) in constant:
                        yield constant.get(''.join(stack))
                        stack = []
                        stack.append(key)

                    elif ''.join(stack) in OPERATORS_func:

                        yield ''.join(stack)
                        stack = []
                        stack.append(key)
                    else:
                        stack.append(key)
        else:

            if stack and (stack[0] in '1234567890.'):
                yield float(''.join(stack))
            elif ''.join(stack) in constant:
                yield constant.get(''.join(stack))
            else:
                yield ''.join(stack)

    def convert_into_reverse_pol_notation(splitted_formula):
        """Covert formula(key) into Reverse Polish notation

        Return iterator

        """

        stack = []
        for token in splitted_formula:
            # replace constant
            if token in constant:
                token = constant.get(''.join(token))

            if token in OPERATORS:
                # choose by priority
                while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc_reverse_pol_notation(converted_formula):
        """Calculate Reverse Polish notation"""

        stack = []
        for token in converted_formula:

            if token in OPERATORS:
                # check function with double arguments
                if token in OPERATORS_double:
                    y, x = stack.pop(), stack.pop()
                    stack.append(OPERATORS[token][1](x, y))
                else:
                    # use function with 1 argument
                    x = stack.pop()
                    stack.append(OPERATORS[token][1](x))
            else:
                stack.append(token)

        return stack[0]

    def check_comparison(formula):
        """Function checks if there are comparison operations"""

        for compare in OPERATORS_compare:
            if compare in formula:
                return OPERATORS_compare.get(compare)(
                    main_count(formula.split(compare)[0]),
                    main_count(formula.split(compare)[1]))

        # start calculation
        return calc_reverse_pol_notation(convert_into_reverse_pol_notation(split_formula(formula_formatting(formula))))

    return check_error(formula) if check_error(formula) else check_comparison(formula)


def main():
    """Use of the module argparse

    For installing the utility pycalc

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("EXPRESSION", help="expression string to evaluate", type=str)
    args = parser.parse_args()

    # start main count with parsed arguments
    print(main_count(args.EXPRESSION))


if __name__ == '__main__':
    print(main_count('fsum([9])'))
