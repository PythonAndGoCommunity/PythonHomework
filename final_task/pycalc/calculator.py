"""Main module of the calculator."""
# TODO: set custom module's higher priority than included (math)

import math
import re


class Calculator:
    """Handles all operations related to the conversion and evaluation
    of expressions."""

    BINARIES = (
        ('^', lambda a, b: a ** b),  # **
        ('//', lambda a, b: a // b),
        ('/', lambda a, b: a / b),
        ('*', lambda a, b: a * b),
        ('%', lambda a, b: a % b),
        ('+', lambda a, b: a + b),
        ('<=', lambda a, b: a <= b),
        ('>=', lambda a, b: a >= b),
        ('<', lambda a, b: a < b),
        ('>', lambda a, b: a > b),
        ('!=', lambda a, b: a != b),
        ('==', lambda a, b: a == b)
    )

    FUNCTIONS = (
        ('pow', lambda a, b, c: pow(a, b)),
        ('abs', lambda a: abs(a)),
        ('round', lambda a: round(a)),
        ('ctan', lambda a: 1 / math.tan(a))
    )

    def __init__(self, validator):
        self._validator = validator
        self._modules = [math]

    def calc_start(self, expression, modules=None):
        """Entry point of calculating. Validates, transforms and finally
        calculates given expression. Returns calculating result."""

        self._validator.validate(expression)
        self.import_modules(modules)
        expression = self.transform(expression)
        expression = self.replace_constants(expression)
        expression = self.calculate_functions(expression)
        expression = self.handle_implicit_multiplication(expression)

        result = self.calculate(expression)
        return self.convert(result)

    def import_modules(self, modules):
        """Imports all modules from given list."""

        if modules is not None:
            for m in modules:
                new_module = __import__(m)
                self._modules.append(new_module)

    def transform(self, expression):
        """Transforms the expression into Calculator friendly form."""

        expression = expression.lower()
        expression = expression.strip("'")
        expression = expression.strip('"')
        expression = expression.replace(' ', '')
        expression = expression.replace('**', '^')
        expression = self.handle_subtraction(expression)

        return expression

    def find_left_num(self, expression, sign_pos):
        """Returns a number that lays left from the sign_pos (or
        None if it doesn't exist."""

        pattern = r'([0-9\[\]\.\-]|(e\+)|(e\-))+$'
        num = re.search(pattern, expression[:sign_pos])
        if num is None:
            self._validator.assert_error(
                "ERROR: please, check your expression.")
        return num.group(0)

    def find_right_num(self, expression, sign_pos):
        """Returns a number that lays right from the sign_pos (or
        None if it doesn't exist."""

        pattern = r'^([0-9\[\]\.\-]|(e\+)|(e\-))+'
        num = re.search(pattern, expression[sign_pos + 1:])
        if num is None:
            self._validator.assert_error(
                "ERROR: please, check your expression.")
        return num.group(0)

    def calculate(self, expression=None):
        """Recursive function that divides the expression, calculates its
        right and left parts and whole result."""

        expression = self.calculate_nested(expression)
        expression = self.handle_extra_signs(expression)

        for sign, func in self.BINARIES:
            while True:
                sign_pos = self.find_sign(expression, sign)
                if sign_pos == -1:
                    break

                if sign == '^':
                    left = self.find_left_num(expression, sign_pos)
                    if left.find(']') == -1:
                        left = left.replace('-', '')
                else:
                    left = self.find_left_num(expression, sign_pos)

                slen = len(sign) - 1
                right = self.find_right_num(expression, sign_pos + slen)

                result = self.calculate_elementary(
                    expression[sign_pos:sign_pos + slen + 1], left, right)
                expression = expression.replace(
                    left + sign + right, str(result), 1)

        return expression.strip('[]')

    def find_sign(self, expression, sign):
        """Returns a position of given sign in the
        expression (-1 if not found)."""

        sign_pos = None
        if sign == '^':
            sign_pos = expression.rfind(sign)
        elif sign == '+':
            sign_pos = expression.find(sign)
            while sign_pos != -1 and expression[sign_pos - 1] == 'e':
                sign_pos = expression[sign_pos + 2:].find(sign)
        else:
            sign_pos = expression.find(sign)

        return sign_pos

    def calculate_functions(self, expression):
        """Calculates all founded functions and returns an expression that
        contains only elementary binary operations."""

        # List reversion here makes it possible to calculate nested functions
        pattern = r'[A-Za-z_]+[A-Za-z0-9_]*'
        func_name_list = re.findall(pattern, expression)[::-1]

        for func_name in func_name_list:
            if func_name in ('False', 'True'):
                continue

            func, is_callable = self.get_func_or_const_by_name(func_name)
            if func is None:
                self._validator.assert_error(
                    "ERROR: no such function " + func_name + ".")

            if is_callable is False:
                continue

            fpos = expression.rfind(func_name)
            args, arg_end = self.get_func_args(expression, func_name, fpos)

            result = ''
            try:
                if args is not None:
                    converted_args = self.convert_arguments(args)
                    result = func(*converted_args)
                else:
                    result = func()
            except TypeError:
                self._validator.assert_error(
                    "ERROR: please, check function " + func_name + ".")

            expression = expression.replace(
                expression[fpos:arg_end], '(' + str(result) + ')', 1
            )

        return expression

    def get_func_args(self, expression, func_name, func_pos):
        """Finds all the arguments of the function, located on the func_pos."""

        arg_start = func_pos + len(func_name)
        arg_end = arg_start + expression[arg_start:].find(')')
        arguments = expression[arg_start:arg_end]

        while arguments.count('(') != arguments.count(')'):
            arg_end += 1 + expression[arg_end:].find(')')
            arguments = expression[arg_start:arg_end]

        argument_list = arguments[1:-1].split(',')
        if '' in argument_list:
            argument_list = None

        return argument_list, arg_end

    def replace_constants(self, expression):
        """Finds constants in imported and user modules and builtins."""

        pattern = r'[A-Za-z_]+[A-Za-z0-9_]*'
        names = re.findall(pattern, expression)

        for n in names:
            obj, is_callable = self.get_func_or_const_by_name(n)
            if is_callable or obj is None:
                continue

            # Parentheses are used to prevent mixing numbers
            # with replaced constants.
            expression = expression.replace(n, '(' + str(obj) + ')')

        return expression

    def get_func_or_const_by_name(self, requested_name):
        """Finds by name and returns a function if it exists, else
        returns None."""

        result = None, None
        for fname, obj in self.FUNCTIONS:
            if fname == requested_name:
                result = obj, True

        for m in self._modules:
            if hasattr(m, requested_name):
                obj = getattr(m, requested_name)
                if callable(obj):
                    result = obj, True
                else:
                    result = obj, False

        return result

    def convert(self, a):
        """Converts an argument to int, bool or float."""

        if not isinstance(a, str):
            return a

        if a in ('True', 'False'):
            a = True if a == 'True' else False
            return a

        try:
            a = int(a)
        except ValueError:
            a = float(a)

        return a

    def convert_arguments(self, args):
        """Returns a list of converted arguments."""

        converted_args = []
        for a in args:
            result_a = self.calculate(a)
            converted_args.append(self.convert(result_a))

        return converted_args

    def handle_subtraction(self, expression):
        """Modifies subtractions in given expression to make them
        calculator friendly."""

        pattern = r'[0-9\]]\-'
        cases = re.findall(pattern, expression)
        for c in cases:
            expression = expression.replace(c, c[0] + '+' + c[1])

        return expression

    def handle_implicit_multiplication(self, expression):
        """Replaces all implicit multiplication cases with obvious ones."""

        patterns = (r'[0-9][A-Za-z][^\-+]', r'\)[0-9]', r'[0-9]\(', r'\)\(')
        for p in patterns:
            cases = re.findall(p, expression)
            for c in cases:
                expression = expression.replace(c, c[0] + '*' + c[1])

        return expression

    def handle_extra_signs(self, expression):
        """Gets rid of extra pluses and minuses in given expression."""

        pattern = r'[-+]{2,}'
        cases = re.findall(pattern, expression)
        for c in cases:
            minus_count = c.count('-')
            if minus_count % 2 == 0:
                expression = expression.replace(c, '+', 1)
            else:
                expression = expression.replace(c, '-', 1)

        expression = self.handle_subtraction(expression)
        return expression

    def calculate_elementary(self, operation, *args):
        """Calculates elementary binary operations like addition, subtraction,
        multiplication, division etc."""

        result = None

        args = list(re.sub(r'[\[\]]', '', a) for a in args)
        args = list(self.handle_extra_signs(a) for a in args)

        converted_args = []
        try:
            converted_args = list(self.convert(a) for a in args)
        except ValueError:
            self._validator.assert_error(
                "ERROR: please, check your expression.")

        self._validator.check(operation, *converted_args)
        for o, func in self.BINARIES:
            if o == operation:
                result = func(*converted_args)
                break

        return result

    def calculate_nested(self, expression):
        """Returns the result of nested expression calculating."""

        while True:
            nested = self.get_nested(expression)
            if nested is None:
                break
            nested_result = self.calculate(nested[1:-1])
            expression = expression.replace(
                nested, '[' + str(nested_result) + ']')

        return expression

    def get_nested(self, expression):
        """Finds and returns nested expression (with no nested inside it) if
         it exists, else returns None."""

        # From '(' to ')' blocking any parentheses inside
        nested = re.search(r'\([^()]*\)', expression)
        return nested.group(0) if nested is not None else None
