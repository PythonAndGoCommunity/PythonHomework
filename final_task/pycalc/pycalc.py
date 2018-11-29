import argparse
import math
import re
import operator
from collections import namedtuple


class ErrorWrongBracketsBalance(Exception):
    pass


class ErrorSpaceBetweenOperands(Exception):
    pass


class ErrorSpaceIn2ElementOperators(Exception):
    pass


class ErrorTokenParseException(Exception):
    pass


class ErrorWrongToken(ValueError):
    pass


class ErrorWrongOperandsCount(ValueError):
    pass


operator_ = namedtuple('operator', ['priority', 'function'])

operators = {
    '+':  operator_(0, operator.add),
    '-':  operator_(0, operator.sub),
    '*':  operator_(1, operator.mul),
    '/':  operator_(1, operator.truediv),
    '^':  operator_(2, operator.pow),
    '//': operator_(0.5, operator.floordiv),
    '%':  operator_(0.5, operator.mod),
}

prefix_func = namedtuple('prefix_function', ['priority', 'function', 'args_count'])

prefix_function = {
    'sin': prefix_func(0, math.sin, 1),
    'cos': prefix_func(0, math.cos, 1),
    'tan': prefix_func(0, math.tan, 1),
    'exp': prefix_func(0, math.exp, 1),
    'acos': prefix_func(0, math.acos, 1),
    'asin': prefix_func(0, math.asin, 1),
    'atan': prefix_func(0, math.atan, 1),
    'sqrt': prefix_func(0, math.sqrt, 1),
    'log': prefix_func(0, math.log, 2),
    'log10': prefix_func(0, math.log10, 1),
    'loglp': prefix_func(0, math.log1p, 1),
    'factorial': prefix_func(0, math.factorial, 1),
    'pow': prefix_func(0, math.pow, 2),
    'abs': prefix_func(0, abs, 1),
    'round': prefix_func(0, round, 1),
}

constants = {
    'pi': math.pi,
    'e': math.e,
}

comparisons = {
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne,
}

unary = {
    '-': operator.neg,
    '+': operator.pos,
}


def get_token(expression='', result_lst=None):
    """
    getting expression in string format and split by simple tokens using recursion

    :param expression: expression in string format
    :param result_lst: None if first function call, else part of expression for ex.'(-1+5)'
    :return: result_lst contains all tokens as list elements    for ex. ['(', '-', '1', '+', '5', ')']
    """
    if result_lst is None:
        expression = expression.lower().replace(' ', '')
        result_lst = []
    el = re.match(r'\)|\(|-\d+\.?\d*|\d+\.?\d*|(--)|-\w*|[-+*/,^]|\.\d+|\w+|\D+|(\d+)\w', expression)
    try:
        el.group()
    except Exception:
        raise ErrorTokenParseException('ERROR: wrong expression')
    if el.group()[-1] == '(':
        el = re.match(r'\D{1,1}', expression)
        result_lst.append(el.group())
    elif el.group() == '--':
        result_lst.append('+')
    elif el.group()[0] == '.':
        result_lst.append('0' + el.group())
    elif el.group() == 'epi':
        result_lst.append('e')
        result_lst.append('pi')
    else:
        result_lst.append(el.group())
    if len(el.group()) < len(expression):
        return get_token(expression[el.end():], result_lst)
    else:
        return result_lst


def check_implicit_mul(tokens):
    """
    gets list contain tokens verify and add if need multiply operator

    :param tokens: list with tokens for ex.['(', '5', ')', '(', '1', ')' ]
    :return: list with tokens and * if add it ['(', '5', ')', '*', '(', '1', ')' ]
    """
    new_tokens = []
    for index, token in enumerate(tokens):

        if token == '(' and index != 0:
            if (type(tokens[index - 1]) is float) or (tokens[index - 1] is ')'):
                new_tokens.append('*')
                new_tokens.append(token)
            else:
                new_tokens.append(token)

        elif token == ')' and index != len(tokens) - 1:
            if (type(tokens[index + 1]) is float) or (tokens[index+1] in prefix_function):
                new_tokens.append(token)
                new_tokens.append('*')
            else:
                new_tokens.append(token)
        elif (type(token) is float) and (index != len(tokens)-1):
            if (type(tokens[index+1]) is float) or (tokens[index+1] in prefix_function):
                new_tokens.append(token)
                new_tokens.append('*')
            else:
                new_tokens.append(token)
        else:
            new_tokens.append(token)
    return new_tokens


def verify_to_elements_operator(expression):
    to_el_operators_separate_whitespace = [
        '< =', '> =', '= =', '* *', '/ /'
    ]
    for el in to_el_operators_separate_whitespace:
        if el in expression:
            raise ErrorSpaceIn2ElementOperators('ERROR: {} is wrong operators'.format(el))
        else:
            continue


def check_space_between_operands(expression=''):
    """
    get expression and verify it has space between 2 operands

    :param expression:
    :return:
    """
    expression = expression.rstrip().lstrip()
    for index, el in enumerate(expression):
        if el == ' ':
            try:
                prev = float(expression[index - 1])
                next_ = float(expression[index + 1])
            except ValueError:
                continue
            if prev and next_:
                raise ErrorSpaceBetweenOperands('ERROR: space between operands')


def brackets_is_balanced(expression):
    """
    verify brackets is balanced or not

    :param expression: in str or list format for ex. ['(', '1', '+', '5', ')']
    :return: True if brackets is balanced else False
    """
    count_open_brackets = expression.count('(')
    count_close_brackets = expression.count(')')
    return count_open_brackets == count_close_brackets


def calculate_expression(expression):
    """
    calculate expression in reverse Polish notation

    :param expression: list contains tokens in reverse Polish notation ['1', '5', '+']
    :return: result
    """
    stack = []
    try:
        while expression:
            token = expression.pop(0)
            if type(token) is float:
                stack.append(token)

            elif token in operators:
                if len(stack) == 1:
                    func = unary[token]
                    operands = (stack.pop(-1),)
                    stack.append(func(*operands))

                elif not stack:
                    func = unary[token]
                    for i, el in enumerate(expression):
                        if type(el) is not float:
                            continue
                        else:
                            operands = (expression.pop(i),)
                            res = func(*operands)
                            expression.insert(i, res)
                else:
                    func = operators[token].function
                    operands = (stack.pop(-2), stack.pop(-1))
                    stack.append(func(*operands))

            elif token in prefix_function:
                func = prefix_function[token]
                if func.args_count == 1:
                    operands = (stack.pop(-1),)
                    stack.append(func.function(*operands))
                elif func.args_count == 2:
                    try:
                        operands = (stack.pop(-2), stack.pop(-1))
                    except IndexError:
                        operands = (stack.pop(-1),)
                    stack.append(func.function(*operands))
        if len(stack) == 1:
            return stack[0]
        else:
            raise ErrorWrongOperandsCount('ERROR: Wrong operands count')
    except Exception as e:
        return e


def convert_num_and_const_to_float(expression):
    """
    converts constants and numbers to float type
    :param expression: may be in list format with simple tokens for ex. ['(', '-', '1', '+', '5', ')']
    :return:
    """
    for index, el in enumerate(expression):
        try:
            if el in constants:
                expression[index] = constants[el]
            elif (el[0] == '-') and (el[1:] in constants):
                expression[index] = operator.neg(constants[el[1:]])
            elif (el[0] == '-' and len(el) != 1) and (type(expression[index - 1]) is float):
                expression.insert(index, '-')
                element = float(expression.pop(index + 1)) * (-1)
                expression.insert(index + 1, element)
            elif (el[0] == '-' and len(el) != 1) and (el[1:] in prefix_function):
                if expression[index - 1] == '(':
                    expression.insert(index, 0.0)
                    expression.insert(index + 1, '-')
                    expression.insert(index + 2, expression.pop(index + 2)[1:])
                else:
                    expression.insert(index, '-')
                    expression.insert(index + 1, expression.pop(index + 1)[1:])
            else:
                try:
                    expression[index] = float(el.replace(',', '.')) if type(el) != float else el
                except ValueError:
                    pass
        except TypeError:
            continue
    return expression


def parse_to_reverse_polish_notation(tokens, postfix_expression=None, stack=None):
    """
    convert infix expression format to reverse Polish notation expression
    :param tokens: list contains simple tokens: numbers is float operators is str
    :param postfix_expression: this list will be return
    :param stack: tmp list for stack operators
    :return: expression in reverse Polish notation
    """
    tokens = convert_num_and_const_to_float(tokens)

    if tokens[-1] in operators or tokens[-1] in prefix_function:
        raise Exception('ERROR: wrong expression')

    if (postfix_expression is None) and (stack is None):
        postfix_expression, stack = [], []

    while len(tokens):
        token = tokens[0]

        if type(token) is float:
            postfix_expression.append(tokens.pop(0))

        elif token in prefix_function:
            stack.append(tokens.pop(0))
        elif token is ',':
            while True:
                try:
                    if stack[-1] is not '(':
                        postfix_expression.append(stack.pop())
                    else:
                        tokens.pop(0)
                        break
                except IndexError:
                    raise ErrorWrongBracketsBalance('ERROR: brackets are not balanced')
        elif token in operators:
            while True:
                if not stack:
                    stack.append(tokens.pop(0))
                    break
                else:
                    tmp = stack[-1]
                    if tmp in operators:
                        if (operators[token].priority <= operators[tmp].priority) and (token != '^'):
                            postfix_expression.append(stack.pop())
                        elif operators[token].priority > operators[tmp].priority:
                            stack.append(tokens.pop(0))
                            break
                        else:
                            stack.append(tokens.pop(0))
                            break
                    elif tmp in prefix_function:
                        postfix_expression.append(stack.pop())
                    elif (len(stack) is 0) or (tmp is '('):
                        stack.append(tokens.pop(0))
                        break
        elif token == '(':
            stack.append(tokens.pop(0))

        elif token == ')':
            tokens.pop(0)
            try:
                index = len(stack) - 1
                while True:
                    if stack[index] != '(' and index != 0:
                        postfix_expression.append(stack.pop())
                        index -= 1
                        if not stack:
                            raise ErrorWrongBracketsBalance
                    else:
                        stack.pop()
                        break
            except Exception as e:
                print(e)
        else:
            raise ErrorWrongToken('ERROR: {token} is not correct element of expression'.format(token=token))

    postfix_expression.extend(stack[::-1])

    return postfix_expression


def split_by_comparison(expression):
    """
    split expressin by comparison operators
    :param expression: expression type is string
    :return: tuple contains parts of expression after splitting and list of comp. operators
    """
    eq = '=='
    ne = '!='
    le = '<='
    ge = '>='
    gt = '>'
    lt = '<'
    expression = re.sub(r'\s', '', expression)
    exp = re.split(r'{lt}|{ge}|{ne}|{eq}|{lt}|{gt}'.format(le=le, ge=ge, ne=ne, eq=eq, lt=lt, gt=gt), expression)
    comparisons_operator = re.findall(r'{lt}|{ge}|{ne}|{eq}|{lt}|{gt}'.format(le=le, ge=ge, ne=ne,
                                                                              eq=eq, lt=lt, gt=gt), expression)
    return exp, comparisons_operator


def comparison_expressions(expresions, comparisons_lst):
    """
    comparison some expressions
    :param expresions:
    :param comparisons_lst:
    :return: bool value
    """
    result = []
    while len(expresions) != 1:
        last_el = expresions.pop()
        befor_last_el = expresions[-1]
        comparison = comparisons[comparisons_lst.pop()]
        result.append(comparison(befor_last_el, last_el))
    while len(result) != 1:
        last_el = result.pop()
        befor_last_el = result.pop()
        result.append(operator.and_(befor_last_el, last_el))
    return result[0]


def from_str_to_result(expression):
    """
    convert and calculate expression step by step
    :param expression: expression type is str
    :return: result or raise Exception if expression has error
    """
    if not brackets_is_balanced(expression):
        raise ErrorWrongBracketsBalance('ERROR: brackets are not balanced')

    expression = get_token(expression)
    expression = convert_num_and_const_to_float(expression)
    expression = check_implicit_mul(expression)
    expression = parse_to_reverse_polish_notation(expression)
    try:
        expression = calculate_expression(expression)
    except ZeroDivisionError as e:
        print('ERROR: {exception}'.format(exception=e))
    return expression


def calculate_and_comparison(expression_list, comparison_lst):
    """
    calculate and comarison all expressions in expression_list
    :param expression_list: list contains expressions to calculate and comparison
    :param comparison_lst: list comparison operators
    :return: result
    """
    calculate_expression_list = [from_str_to_result(el) for el in expression_list]
    return comparison_expressions(calculate_expression_list, comparison_lst)


def main():
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', action="store", help="expression string to evaluate")
    args = parser.parse_args()
    if args.EXPRESSION is not None:
        try:
            expression = args.EXPRESSION
            verify_to_elements_operator(expression)
            check_space_between_operands(expression)
            expressions, comparison = split_by_comparison(expression)
            if not comparison:
                print(from_str_to_result(expressions[0]))
            else:
                print(calculate_and_comparison(expressions, comparison))
        except Exception as exception:
            print(exception)
            return exception


if __name__ == '__main__':
    main()
