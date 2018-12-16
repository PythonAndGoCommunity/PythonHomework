import math
import re
import types
import pickle
import argparse
import inspect
from collections import namedtuple


class PyCalc:
    """
    Python calculator class.
    Evaluates the passed string.

    List of methods:
    __init__                - class initializer;
    tokenizer               - creates list of tokens from passed string;
    rpn - transforms passed stack into reverse polish notation stack;
    execute_rpn             - executes passed stack (stack have to be an rpn stack)
    calculate               - calculates passed string using previous methods;

    @static_method
    get_math_operatros      - transforms math module in following dictionary:
        {'name': namedtuple("full_info", ("func", "priority", "number_args", "regex", "tag")};
    lexer                   - transforms string into token stack. This method is more common, while tokenizer
        has more rules to perform.
    """

    def __init__(self, *args):
        """
        Pycalc class initializer.
        Sets a lot of variables, such as tag variables, dictionaries of math operators, math constants, etc. and saves
        them into pickle file. On the next run this file'll be unpacked and loaded, so there'll be no need to recalcula-
        te dictionaries of math operators and constants. After this method parses all passed modules and retrieves
        functions and constants form them. User functions and constants won't be added to pickle file.

        Arguments:
            *args - (list) list of additional modules.

        Returns:
            No returns.

        Raises:
            No raises.
        """

        full_info = namedtuple("full_info", ("func", "priority", "number_args", "regex", "tag"))
        regex_and_tag = namedtuple("regex_and_tag", ("regex", "tag"))

        cfg_name = "operators.pkl"

        tag_advanced = 'advanced'
        tag_constant = 'constant'
        tag_common = 'common'
        tag_number = 'number'

        math_priority = 8

        try:

            with open(cfg_name, 'rb') as pickle_file:
                obj = pickle.load(pickle_file)
                math_constants, math_operators, token_expressions = obj

        except Exception:

            common_operators = {

                ",": full_info(None, 9, None, r',', tag_common),

                "abs": full_info(float.__abs__, 8, 1, r'abs', tag_common),
                "round": full_info(float.__round__, 8, 1, r'round', tag_common),

                "$": full_info(float.__pos__, 7, 1, r'\$', tag_common),
                "#": full_info(float.__neg__, 7, 1, r'\#', tag_common),

                "^": full_info(float.__pow__, 6, 2, r'\^', tag_common),

                "*": full_info(float.__mul__, 5, 2, r'\*', tag_common),
                "/": full_info(float.__truediv__, 5, 2, r'/', tag_common),

                "%": full_info(float.__mod__, 4, 2, r'%', tag_common),
                "//": full_info(float.__floordiv__, 4, 2, r'//', tag_common),

                "-": full_info(float.__sub__, 2, 2, r'-', tag_common),
                "+": full_info(float.__add__, 2, 2, r'\+', tag_common),

                "(": full_info(None, 1, 0, r'\(', tag_common),

                "<=": full_info(float.__le__, 0, 2, r'<=', tag_common),
                ">=": full_info(float.__ge__, 0, 2, r'>=', tag_common),
                "==": full_info(float.__eq__, 0, 2, r'==', tag_common),
                "!=": full_info(float.__ne__, 0, 2, r'!=', tag_common),
                "<": full_info(float.__lt__, 0, 2, r'<', tag_common),
                ">": full_info(float.__gt__, 0, 2, r'>', tag_common),

                ")": full_info(None, None, None, r'\)', tag_common),
                "space": full_info(None, None, None, r'[ \n\t]+', None),
                "num_i": full_info(None, None, None, r'[0-9]+', tag_number),
                "num_f": full_info(None, None, None, r'[0-9]+\.[0-9]+', tag_number),
                "num_f2": full_info(None, None, None, r'\.[0-9]+', tag_number),
                "num_f3": full_info(None, None, None, r'[0-9]+\.', tag_number)
            }

            math_operators, math_constants = PyCalc.get_operators_from_module(module=math,
                                                                              priority=math_priority,
                                                                              tag_operators=tag_advanced,
                                                                              tag_constants=tag_constant,
                                                                              tuple_template=full_info
                                                                              )

            math_operators.update(common_operators)

            token_expressions = []
            for item in math_operators.values():
                token_expressions.append(regex_and_tag(item.regex, item.tag))
            for item in math_constants.values():
                token_expressions.append(regex_and_tag(item.regex, item.tag))
            token_expressions.sort(reverse=True)

            try:
                obj = [math_constants,
                       math_operators,
                       token_expressions]
                with open(cfg_name, 'wb') as pickle_file:
                    pickle.dump(obj, pickle_file)
            except Exception:
                pass

        finally:

            if args:

                for item in args:
                    temp_operators, temp_constants = PyCalc.get_operators_from_module(module=item,
                                                                                      priority=math_priority,
                                                                                      tag_operators=tag_advanced,
                                                                                      tag_constants=tag_constant,
                                                                                      tuple_template=full_info)
                    math_operators.update(temp_operators)
                    math_constants.update(temp_constants)
                    for j_item in temp_operators.values():
                        token_expressions.append(regex_and_tag(j_item.regex, j_item.tag))
                    for j_item in temp_constants.values():
                        token_expressions.append(regex_and_tag(j_item.regex, j_item.tag))
                token_expressions.sort(reverse=True)

            self.token_expressions = token_expressions
            self.constants = math_constants
            self.operators = math_operators

            self.tag_common = tag_common
            self.tag_advanced = tag_advanced
            self.tag_number = tag_number
            self.tag_constant = tag_constant

    def tokenizer(self, input_string):
        """
        Creates list of tokens from passed string. Lexer method is used as common tokenizer. Adds a lot of additional
        rules such as checking unary operations, logs, bracket balance etc to lexer result.

        Arguments:
            input_string - (string) input string with math expression.

        Returns:
            tokens - (list) list of tokens from passed string.

        Raises:
            RuntimeError - Unknown syntax! - in case of spaces between numbers.
            RuntimeError - Brackets aren't balanced! - in case of unbalanced brackets.
        """
        # Checking spaces between numbers
        pattern = r"[0-9][ \n\t]+[0-9]"
        if re.search(pattern, input_string):
            raise RuntimeError("Unknown syntax: " + re.search(pattern, input_string).group(0))

        # Checking unary operations
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

        # Lexing
        token_and_tag = namedtuple("token_and_tag", ("token", "tag"))
        token_stack = PyCalc.lexer(input_string, self.token_expressions, token_and_tag)

        # Checking bracket balance, adding implicit multiplications, replacing unary operations
        temporary_stack = ["$"]
        prev_item = token_and_tag("$", self.tag_common)
        bracket_balance = 0

        for index, item in enumerate(token_stack):

            if item.token == "(":
                bracket_balance += 1
            elif item.token == ")":
                bracket_balance -= 1
                if bracket_balance < 0:
                    raise RuntimeError("Brackets aren't balanced!")

            if ((item.tag == self.tag_constant or item.tag == self.tag_advanced or item.tag == self.tag_number) and
                (prev_item.token == ")" or prev_item.tag == self.tag_constant or prev_item.tag == self.tag_number)) or \
                    ((prev_item.tag == self.tag_constant or prev_item.tag == self.tag_number) and item.token == "("):
                temporary_stack.append("*")

            if prev_item.tag == self.tag_common and prev_item.token != ")":
                if item.token == "+":
                    continue
                elif item.token == "-":
                    temporary_stack.append("#")
                    continue

            temporary_stack.append(item.token)
            prev_item = item
        else:
            token_stack = temporary_stack[1:]
            if bracket_balance != 0:
                raise RuntimeError("Brackets aren't balanced!")

        # Solving the log problem
        i = 0
        while i < len(token_stack):
            if token_stack[i] == "log":
                j = i+2
                bracket_counter = 1
                while bracket_counter != 0:
                    if token_stack[j] == "(":
                        bracket_counter += 1
                    elif token_stack[j] == ")":
                        bracket_counter -= 1
                    elif token_stack[j] == "," and bracket_counter == 1:
                        break

                    j += 1

                else:
                    token_stack.insert(j-1, ",")
                    token_stack.insert(j, "e")

            i += 1

        return token_stack

    def rpn(self, stack):
        """
        Transforms list of tokens to its rpn (reverse polish notation) form. Uses common RPN algorithm.

        Arguments:
            stack - (list) input stack of tokens.

        Returns:
            string_as_stack - (list) list of tokens in rpn form.

        Raises:
            No raises.
        """

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
                elif self.operators[temporary_stack[-1]].priority <= self.operators[item].priority and item == "^":
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
        """
        Executes passed stack in rpn form and returns the result or raises error. Uses common RPN-execution algorithm.

        Arguments:
            rpn_stack - (list) input stack of tokens in rpn form.

        Returns:
            result - (float) resulting number.

        Raises:
            RuntimeError - Unknown operation! - in case of wrong operation oder.
            ZeroDivision - in case of division by zero.
            IndexError - in case of wrong operation oder.
            ValueError - in case of wrong operand.
        """

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
            raise RuntimeError("Resulting stack isn't empty. Unknown operation!")

        return result

    def calculate(self, input_string):
        """
        Calculates passed string and takes care of all errors, that happens in program running time.

        Arguments:
            input_string - (string) input string with math expression.

        Returns:
            result - (float) resulting number.

        Raises:
            No raises.
        """

        try:
            tokens = self.tokenizer(input_string)
        except Exception as eerror:
            print("ERROR: in tokenizer" + str(eerror.args[0]))
            exit(1)

        rpn = self.rpn(tokens)

        try:
            result = self.execute_rpn(rpn)
        except IndexError:
            print("ERROR: in execute_rpn Wrong operations order!")
            exit(1)
        except ZeroDivisionError:
            print("ERROR: in execute_rpn Division by zero!")
            exit(1)
        except RuntimeError as rerror:
            print("ERROR: in execute_rpn " + str(rerror.args[0]))
            exit(1)
        except ValueError:
            print("ERROR: in execute_rpn Unknown operand!")
            exit(1)
        except Exception:
            print("ERROR: in execute_rpn Unknown error!")
            exit(1)

        return result

    @staticmethod
    def get_operators_from_module(module, priority, tag_operators, tag_constants, tuple_template):
        """
        Parses passed module and returns dictionary with followed structure:
            {'name': ("func", "priority", "number_args", "regex", "tag")}
        Uses namedtuple to create more readable code.

        Arguments:
            module - (module) input module to parse;
            priority - (int) priority of math operations. As math module has only functions - all of functions'll
                have the same priority;
            tag_operators - (string) string tag for operators;
            tag_constants - (string) string tag for constants;
            tuple_template - template of tuple to create cool tuples in return dictionary.

        Returns:
            operators - (dict) dictionary of operators.
            constants - (dict) dictionary of constants.

        Raises:
            No raises.
        """
        any_pattern = r"\(.+\)"
        brackets_pattern = r"\(.*\)"
        coma_pattern = r"\,"

        operators = {}
        constants = {}

        for item in dir(module):
            if isinstance(module.__dict__.get(item), types.BuiltinFunctionType):
                if item.find("__"):
                    res = re.search(brackets_pattern, module.__dict__.get(item).__doc__)
                    if re.search(any_pattern, res.group()):
                        res = re.findall(coma_pattern, res.group())
                        operators.update({item: tuple_template(module.__dict__.get(item), priority, len(res) + 1,
                                                               item, tag_operators)})
                    else:
                        operators.update({item: tuple_template(module.__dict__.get(item), priority, 0,
                                                               item, tag_operators)})
            elif isinstance(module.__dict__.get(item), types.FunctionType):
                res = len(inspect.getfullargspec(module.__dict__.get(item)).args)
                operators.update({item: tuple_template(module.__dict__.get(item), priority, res, item, tag_operators)})
            else:
                if item.find("__"):
                    constants.update({item: tuple_template(module.__dict__.get(item), None, None, item, tag_constants)})
        return operators, constants

    @staticmethod
    def lexer(characters, token_expressions, tuple_template):
        """
        Creates list of tokens from passed string.

        Arguments:
            characters - (string) input string with math expression.
            token_expressions - (list) input list with regulary expressions of math operands, constants and numbers.
            tuple_template - template of tuple to create cool tuples from received data.

        Returns:
            tokens - (list) list of tokens from passed string.

        Raises:
            RuntimeError - Illegal character! - in case of unknown math operand or operator.
        """

        pos = 0
        tokens = []
        while pos < len(characters):
            match = None
            for token_expr in token_expressions:
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
                raise RuntimeError('ERROR in lexer: Illegal character: %s\n' % characters[pos])
            else:
                pos = match.end(0)
        return tokens


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("EXPRESSION", help="expression string to evaluate")
    parser.add_argument('-m', '--use-module', metavar='MODULE', type=str, nargs='+', help='additional user modules')
    args = parser.parse_args()
    module_list = []
    if args.use_module:
        for item in args.use_module:
            module_list.append(__import__(item))

    calc = PyCalc(*module_list)
    result = calc.calculate(args.EXPRESSION)
    print(result)


if __name__ == '__main__':
    main()
