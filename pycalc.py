import math
import re
import sys
import argparse

# list of operations
operations = {'+': 2, '-': 2, '*': 3, '/': 3, '//': 0, '%': 3, '^': 4, '<': 1, '>': 1, '<=': 1, '>=': 1, '==': 1,
              '!=': 1, '(': 0, ')': 0, 'sin': 4, 'cos': 4, 'tan': 4, 'exp': 4, 'log': 4, 'loglp': 4, 'log10': 4,
              'sqrt': 4, 'asin': 4, 'acos': 4, 'atan': 4, 'atan2': 4, 'hypot': 4, 'degrees': 4, 'radians': 4,
              'acosh': 4, 'asinh': 4, 'atanh': 4, 'cosh': 4, 'sinh': 4, 'tanh': 4, 'round': 4, 'abs': 4}
constant_pi = 'pi'


# use regular expression to divide input string
def split(exp):
    return re.split('([()!<>=^%*/+-])', exp.replace(" ", ""))


# check if operand is number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# check if the symbol is in list of operations
def is_operation(s):
    if s in operations.keys():
        return True


# check if operand is pi
def is_constant_pi(s):
    if s == constant_pi:
        return True


# check if stack is not empty
def is_not_stack_empty(stack):
    return stack != []


# parse list by algorithm of reverse polish notation
def parse(exp):
    # list of operations(named as 'stack' because of algorithm)
    operations_stack = []
    # named as 'array' because of algorithm
    output_array = []
    counter_of_open_brackets = 0
    counter_of_close_brackets = 0

    for element in exp:
        if is_number(element):
            output_array.append(float(element))

        if is_constant_pi(element):
            output_array.append(math.pi)

        if is_operation(element):
            if element == '(':
                counter_of_open_brackets = counter_of_open_brackets + 1
            # deleting ()
            if is_not_stack_empty(operations_stack):
                if element == ')':
                    counter_of_close_brackets = counter_of_close_brackets + 1
                    previous = operations_stack.pop()
                    while previous != '(':
                        if previous != '(':
                            output_array.append(previous)
                        previous = operations_stack.pop()
                else:
                    # check previous operand in stack
                    previous = operations_stack.pop()
                    # if it't sign of comparison
                    if element == '=' and previous == '!':
                        operations_stack.append('!=')
                    if element == '=' and previous == '=':
                        operations_stack.append('==')
                    if element == '=' and previous == '<':
                        operations_stack.append('<=')
                    if element == '=' and previous == '>':
                        operations_stack.append('>=')
                    if element == '/' and previous == '/':
                        operations_stack.append('//')
                    # if previous' priority is bigger - push from operations
                    elif operations[previous] >= operations[element] and element != '(':
                        output_array.append(previous)
                        operations_stack.append(element)
                    else:
                        # else store all
                        operations_stack.append(previous)
                        operations_stack.append(element)
            else:
                operations_stack.append(element)
    # make result list
    while is_not_stack_empty(operations_stack):
        output_array.append(operations_stack.pop())
    # check number of brackets
    if counter_of_open_brackets != counter_of_close_brackets:
        print("ERROR: Brackets are not balanced")
        sys.exit(1)
    return output_array


# +
def add(first, second):
    return first + second


# -
def subtract(first, second):
    return first - second


# *
def multiply(first, second):
    return first * second


# /
def divide(first, second):
    try:
        return first / second
    except ZeroDivisionError:
        print("ERROR: Zero division")
        sys.exit(1)


# //
def get_whole_part_from_division(first, second):
    try:
        return first // second
    except ZeroDivisionError:
        print("ERROR: Zero division")
        sys.exit(1)


# compare operands
def comparison(operator, first, second):
    if operator == '<':
        return first < second
    if operator == '>':
        return first > second
    if operator == '<=':
        return first <= second
    if operator == '>=':
        return first >= second
    if operator == '==':
        return first == second
    if operator == '!=':
        return first != second


# use functions from module math
def function_from_module_math(func, operand):
    try:
        if func == 'sin':
            return math.sin(operand)
        if func == 'cos':
            return math.cos(operand)
        if func == 'tan':
            try:
                return math.tan(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated tan")
                sys.exit(1)
        if func == 'exp':
            return math.exp(operand)
        if func == 'log':
            try:
                return math.log(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated log")
                sys.exit(1)
        if func == 'loglp':
            try:
                return math.loglp(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated loglp")
                sys.exit(1)
        if func == 'log10':
            try:
                return math.log10(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated log10")
                sys.exit(1)
        if func == 'sqrt':
            try:
                return math.sqrt(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated sqrt")
                sys.exit(1)
        if func == 'asin':
            try:
                return math.asin(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated asin")
                sys.exit(1)
        if func == 'acos':
            try:
                return math.acos(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated acos")
                sys.exit(1)
        if func == 'atan':
            try:
                return math.atan(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated atan")
                sys.exit(1)
        if func == 'atan2':
            try:
                return math.atan2(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated atan2")
                sys.exit(1)
        if func == 'hypot':
            try:
                return math.hypot(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated hypot")
                sys.exit(1)
        if func == 'degrees':
            return math.degrees(operand)
        if func == 'radians':
            return math.radians(operand)
        if func == 'acosh':
            try:
                return math.acosh(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated acosh")
                sys.exit(1)
        if func == 'asinh':
            try:
                return math.asinh(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated asinh")
                sys.exit(1)
        if func == 'atanh':
            try:
                return math.atanh(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated atanh")
                sys.exit(1)
        if func == 'sinh':
            try:
                return math.sinh(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated sinh")
                sys.exit(1)
        if func == 'cosh':
            try:
                return math.cosh(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated cosh")
                sys.exit(1)
        if func == 'tanh':
            try:
                return math.tanh(operand)
            except ValueError:
                print("ERROR: Trying to take deprecated tanh")
                sys.exit(1)
        if func == 'abs':
            return math.fabs(operand)
        if func == 'round':
            return round(operand)
    finally:
        pass


# calculate reverse polish notation
def calculate(exp):
    stack = parse(split(exp))
    result = []
    stack.reverse()
    if not is_not_stack_empty(stack):
        print("ERROR: No operands")
        sys.exit(1)
    while is_not_stack_empty(stack):
        element = stack.pop()
        if is_operation(element):
            if is_not_stack_empty(result):
                # perform operation from module math
                second_operand = result.pop()
                if operations[element] == 4:
                    output = function_from_module_math(element, second_operand)
                    if output is not None:
                        result.append(output)
                else:
                    # perform simple operetions
                    if is_not_stack_empty(result):
                        first_operand = result.pop()
                        if operations[element] == 1:
                            return comparison(element, first_operand, second_operand)
                        if element == '+':
                            result.append(add(first_operand, second_operand))
                        if element == '-':
                            result.append(subtract(first_operand, second_operand))
                        if element == '*':
                            result.append(multiply(first_operand, second_operand))
                        if element == '/':
                            result.append(divide(first_operand, second_operand))
                        if element == '//':
                            result.append(get_whole_part_from_division(first_operand, second_operand))
                        if element == '^':
                            try:
                                result.append(math.pow(first_operand, second_operand))
                            except ValueError:
                                print("ERROR: Trying to power 0 in 0")
                                sys.exit(1)
                    elif element == '-':
                        result.append(0 - second_operand)
            else:
                print("ERROR: in spelling of operations")
                sys.exit(1)

        else:
            result.append(element)
    # check if all operands were used
    if not is_not_stack_empty(result):
        print("ERROR: in number of operations")
        sys.exit(1)

    # round result if it is necessary
    res = round(result.pop(), 10)
    if res.is_integer():
        return int(res)
    return res


def main():
    argParser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    argParser.add_argument('EXPRESSION', help='expression string to evaluate', type=str)
    args = argParser.parse_args()
    expression = args.EXPRESSION
    print(calculate(expression))


if __name__ == '__main__':
    main()
