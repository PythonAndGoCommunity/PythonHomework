"""Main module of the calculator."""

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

    BUILTINS = (
        ('pow', lambda a, b, c: pow(a, b)),
        ('abs', lambda a: abs(a)),
        ('round', lambda a: round(a)),
        ('ctan', lambda a: 1 / math.tan(a))
    )

    def __init__(self, validator, modules=None):
        """Initializes validator and user modules."""

        self._validator = validator
        self._modules = [math]
        self.import_modules(modules)
        self._constants = self.get_reserved(c=False)
        self._functions = self.get_reserved(c=True)

    def calc_start(self, expression):
        """Entry point of calculating. Validates, transforms and finally
        calculates given expression. Returns calculating result."""

        self._validator.validate(expression)

        expression = self.transform(expression)
        expression = self.replace_constants(expression)
        expression = self.calculate_functions(expression)

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
            self._validator.assert_error("please, check your expression.")
        return num.group(0)

    def find_right_num(self, expression, sign_pos):
        """Returns a number that lays right from the sign_pos (or
        None if it doesn't exist."""

        pattern = r'^([0-9\[\]\.\-]|(e\+)|(e\-))+'
        num = re.search(pattern, expression[sign_pos + 1:])
        if num is None:
            self._validator.assert_error("please, check your expression.")
        return num.group(0)

    def calculate(self, expression=None):
        """Recursive function that divides the expression, calculates its
        right and left parts and whole result."""

        expression = self.calculate_nested(expression)
        expression = self.handle_implicit_multiplication(expression)
        expression = self.handle_extra_signs(expression)

        for sign, func in self.BINARIES:
            while True:
                sign_pos = self.find_sign_pos(expression, sign)
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

    def find_sign_pos(self, expression, sign):
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

            func = None
            if func_name in self._functions:
                func = self.get_reserved_by_name(func_name)
            else:
                self._validator.assert_error(
                    "no such function " + func_name + ".")

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
                    "please, check function " + func_name + ".")

            expression = expression.replace(
                expression[fpos:arg_end], '(' + str(result) + ')', 1
            )

        return expression

    def get_func_args(self, expression, func_name, func_pos):
        """Finds all the arguments of the function,
        located on the func_pos (including nested ones)."""

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

    def get_reserved(self, c=False):
        """Returns a list of all the constants found in imported modules."""

        result = []
        for m in self._modules:
            for d in dir(m):
                obj = getattr(m, d)
                if callable(obj) is c and not d.startswith('_'):
                    result.append(d)

        if c:
            for func_name, _ in self.BUILTINS:
                result.append(func_name)

        # Sort here is used to prevent replacing
        # letters of long reserved names
        result.sort(key=lambda a: len(a), reverse=True)
        return result

    def replace_constants(self, expression):
        """Finds constants in imported and user modules and builtins."""

        const_pattern = '|'.join(self._constants)
        func_pattern = '|'.join(self._functions)
        pattern = r'[A-Za-z_]+[A-Za-z0-9_]*'

        cases = re.finditer(pattern, expression)
        for case in cases:
            c_str = case.group()
            c_pos = case.start()

            # Upper is used to prevent replacing
            # letters in functions (e. g. "eexp(e)")
            replaced = c_str
            funcs = re.findall(func_pattern, replaced)
            for f in funcs:
                replaced = re.sub(f, f.upper(), replaced)

            constants = re.findall(const_pattern, c_str)
            for const in constants:
                obj = self.get_reserved_by_name(const)
                replaced = replaced.replace(const, '(' + str(obj) + ')')

            expression = expression[:c_pos] \
                + expression[c_pos:].replace(c_str, replaced, 1)

        return expression.lower()

    def get_reserved_by_name(self, requested_name):
        """Finds a function or constant by name."""

        for m in self._modules:
            if hasattr(m, requested_name):
                obj = getattr(m, requested_name)
                return obj

        for func_name, func in self.BUILTINS:
            if func_name == requested_name:
                return func

    @staticmethod
    def convert(a):
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
            result_a = self.calc_start(a)
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

        patterns = (
            r'[0-9][A-Za-z][^\-+]', r'[\)\]][0-9]',
            r'[0-9][\[\(]', r'\)\(|\]\['
        )
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
            self._validator.assert_error("please, check your expression.")

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
                nested, '[' + str(nested_result) + ']', 1)

        return expression

    @staticmethod
    def get_nested(expression):
        """Finds and returns nested expression (with no nested inside it) if
         it exists, else returns None."""

        # From '(' to ')' blocking any parentheses inside
        nested = re.search(r'\([^()]*\)', expression)
        return nested.group(0) if nested is not None else None
