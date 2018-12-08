import math
import re
import types
import pickle

from collections import namedtuple


class PyCalc:

    def __init__(self):

        full_info = namedtuple("full_info", ("func", "priority", "number_args", "regex", "tag"))
        regex_and_tag = namedtuple("regex_and_tag", ("regex", "tag"))

        cfg_name = "operators.pkl"

        self.tag_advanced = 'advanced'
        self.tag_constant = 'constant'
        self.tag_common = 'common'
        self.tag_number = 'number'

        try:

            with open(cfg_name, 'rb') as pickle_file:
                obj = pickle.load(pickle_file)
                self.constants, self.operators, self.token_exprs = obj

        except Exception:

            math_priority = 8

            common_operators = {

                ",":        full_info(None,                 9, None,     r',', self.tag_common),


                "abs":      full_info(float.__abs__,        8, 1,        r'abs', self.tag_common),
                "round":    full_info(float.__round__,      8, 1,        r'round', self.tag_common),

                "$":        full_info(float.__pos__,        7, 1,        r'\$', self.tag_common),
                "#":        full_info(float.__neg__,        7, 1,        r'\#', self.tag_common),

                "^":        full_info(float.__pow__,        6, 2,        r'\^', self.tag_common),

                "*":        full_info(float.__mul__,        5, 2,        r'\*', self.tag_common),
                "/":        full_info(float.__truediv__,    5, 2,        r'/', self.tag_common),

                "%":        full_info(float.__mod__,        4, 2,        r'%', self.tag_common),
                "//":       full_info(float.__floordiv__,   4, 2,        r'//', self.tag_common),

                "-":        full_info(float.__sub__,        2, 2,        r'-', self.tag_common),
                "+":        full_info(float.__add__,        2, 2,        r'\+', self.tag_common),



                "(":        full_info(None,                 1, 0,        r'\(', self.tag_common),

                "<=":       full_info(float.__le__,         0, 2,        r'<=', self.tag_common),
                ">=":       full_info(float.__ge__,         0, 2,        r'>=', self.tag_common),
                "==":       full_info(float.__eq__,         0, 2,        r'==', self.tag_common),
                "!=":       full_info(float.__ne__,         0, 2,        r'!=', self.tag_common),
                "<":        full_info(float.__lt__,         0, 2,        r'<', self.tag_common),
                ">":        full_info(float.__gt__,         0, 2,        r'>', self.tag_common),

                ")":        full_info(None,                 None, None,  r'\)', self.tag_common),

                "space":    full_info(None,                 None, None,  r'[ \n\t]+',        None),
                "int_n":    full_info(None,                 None, None,  r'[0-9]+',          self.tag_number),
                "int_f":    full_info(None,                 None, None,  r'[0-9]+\.[0-9]',   self.tag_number),
                "int_f2":   full_info(None,                 None, None,  r'\.[0-9]',         self.tag_number),


            }

            math_operators, math_constants = PyCalc.get_math_operators(math_priority=math_priority,
                                                                       tag_operators=self.tag_advanced,
                                                                       tag_constants=self.tag_constant,
                                                                       tuple_template=full_info
                                                                       )

            self.operators = common_operators
            self.operators.update(math_operators)
            self.constants = math_constants

            token_expressions = []
            for item in self.operators.values():
                token_expressions.append(regex_and_tag(item.regex, item.tag))
            for item in self.constants.values():
                token_expressions.append(regex_and_tag(item.regex, item.tag))

            token_expressions.sort(reverse=True)
            self.token_exprs = token_expressions

            try:
                obj = [self.constants,
                       self.operators,
                       self.token_exprs]
                with open(cfg_name, 'wb') as pickle_file:
                    pickle.dump(obj, pickle_file)
            except Exception:
                pass

    def stack_from_string(self, input_string):

        pattern = r"[0-9][ \n\t]+[0-9]"
        if re.search(pattern, input_string):
            raise RuntimeError("ERROR: Unknown syntax!")

        patterns_and_replacements = [
            (r"--", r"+"),
            (r"\++\+", r"+"),
            (r"\+-", r"-"),
            (r"-\+", r"-"),
            (r"\)\(", r")*(")
        ]

        break_bool = True
        while break_bool:
            break_bool = False
            for item in patterns_and_replacements:
                input_string = re.sub(item[0], item[1], input_string)
            for item in patterns_and_replacements:
                if re.search(item[0], input_string):
                    break_bool = True
                    break

        str_and_tag = namedtuple("str_and_tag", ("s", "tag"))
        string_as_stack = PyCalc.lexer(input_string, self.token_exprs, str_and_tag)

        temporary_stack = ["$"]
        prev_item = str_and_tag("$", self.tag_common)
        bracket_balance = 0

        for index, item in enumerate(string_as_stack):

            if item.s == "(":
                bracket_balance += 1
            elif item.s == ")":
                bracket_balance -= 1
                if bracket_balance < 0:
                    raise RuntimeError("ERROR: brackets aren't balanced!")

            if ((item.tag == self.tag_constant or item.tag == self.tag_advanced or item.tag == self.tag_number) and
                (prev_item.s == ")" or prev_item.tag == self.tag_constant or prev_item.tag == self.tag_number)) or \
               ((prev_item.tag == self.tag_constant or prev_item.tag == self.tag_number) and item.s == "("):
                temporary_stack.append("*")

            if prev_item.tag == self.tag_common and prev_item.s != ")":
                if item.s == "+":
                    continue
                elif item.s == "-":
                    temporary_stack.append("#")
                    continue

            temporary_stack.append(item.s)
            prev_item = item
        else:
            string_as_stack = temporary_stack[1:]
            if bracket_balance != 0:
                raise RuntimeError("ERROR: brackets aren't balanced!")

        return string_as_stack

    def rpn_from_stacked_string(self, stack):

        temporary_stack = []
        rpn_stack = []

        for item in stack:

            if item not in self.operators:
                rpn_stack.append(item)
            elif temporary_stack:

                if item == ")":
                    temp = temporary_stack.pop()
                    while temp != "(":
                        rpn_stack.append(temp)
                        temp = temporary_stack.pop()
                elif item == "(":
                    temporary_stack.append(item)
                elif item == ",":
                    while temporary_stack[-1] != "(":
                        rpn_stack.append(temporary_stack.pop())
                elif self.operators[temporary_stack[-1]].priority <= self.operators[item].priority:
                    temporary_stack.append(item)
                else:
                    temp_priority = self.operators[item].priority
                    while temporary_stack and self.operators[temporary_stack[-1]].priority >= temp_priority:
                        rpn_stack.append(temporary_stack.pop())
                    else:
                        temporary_stack.append(item)
            else:
                temporary_stack.append(item)
        else:
            while temporary_stack:
                rpn_stack.append(temporary_stack.pop())

        return rpn_stack

    def execute_rpn(self, rpn_stack):

        temporary_stack = []

        for item in rpn_stack:

            # print(item+":"+str(temporary_stack))

            if item in self.constants:
                temporary_stack.append(self.constants[item].func)
                continue
            elif item in self.operators:

                count = self.operators[item].number_args
                args = []
                for i in range(count):
                    args.append(float(temporary_stack.pop()))
                args.reverse()
                result = self.operators[item].func(*args)

                temporary_stack.append(result)
            else:
                temporary_stack.append(item)

        result = temporary_stack.pop()
        if temporary_stack:
            raise RuntimeError("ERROR: Unknown operation!")

        return result

    def calculate(self, input_string):

        # print(input_string)
        try:
            stacked_string = self.stack_from_string(input_string)
        except RuntimeError as rerror:
            print(rerror.args[0])
            exit(1)
        except ValueError as verror:
            print(verror.args[0])
            exit(1)
        # print(stacked_string)
        stacked_rpn = self.rpn_from_stacked_string(stacked_string)
        # print(stacked_rpn)
        try:
            result = self.execute_rpn(stacked_rpn)
        except IndexError:
            print("ERROR: Wrong operations order!")
            exit(1)
        except ZeroDivisionError:
            print("ERROR: Division by zero!")
            exit(1)
        except RuntimeError as rerror:
            print(rerror.args[0])
            exit(1)
        return result

    @staticmethod
    def get_math_operators(math_priority, tag_operators, tag_constants, tuple_template):
        """
        Returns dictionary:
        {"operation_name": (math.operation_name, self.number_of_operation's arguments, operation's value)}
        """

        pattern = r"\(.*\)"
        coma_pattern = r"\,"

        math_operators = {}
        math_constants = {}

        for item in dir(math):
            if isinstance(math.__dict__.get(item), types.BuiltinFunctionType):

                if item.find("__"):
                    res = re.search(pattern, math.__dict__.get(item).__doc__)
                    res = re.findall(coma_pattern, res.group())
                    math_operators.update({item: tuple_template(math.__dict__.get(item), math_priority, len(res) + 1,
                                                                item, tag_operators)})

            else:
                if item.find("__"):
                    math_constants.update({item: tuple_template(math.__dict__.get(item), None, None, item,
                                                                tag_constants)})

        return math_operators, math_constants

    @staticmethod
    def lexer(characters, token_exprs, tuple_template):
        pos = 0
        tokens = []
        while pos < len(characters):
            match = None
            for token_expr in token_exprs:
                pattern, tag = token_expr
                regex = re.compile(pattern)
                match = regex.match(characters, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        token = tuple_template(text, tag)
                        tokens.append(token)
                    break
            if not match:
                raise RuntimeError('Illegal character: %s\n' % characters[pos])
            else:
                pos = match.end(0)
        return tokens
