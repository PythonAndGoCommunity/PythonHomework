from pycalc.operators import Operator, Function, Constant
from pycalc.parser import Parser
from pycalc.importmodules import FunctionParser
from pycalc.validator import Validator
from inspect import getfullargspec


def infix_to_postfix(parsed_exp):
    stack = []
    postfix_list = []
    for token in parsed_exp:
        if isinstance(token, Operator) or isinstance(token, Function):
            if token.name == '(':
                stack.append(token)
            elif token.name == ')':
                while stack and stack[-1].name != '(':
                    postfix_list.append(stack.pop())
                if stack:
                    stack.pop()
            else:
                if not token.associativity == 1:
                    while stack and token.priority < stack[-1].priority:
                        postfix_list.append(stack.pop())
                else:
                    while stack and token.priority <= stack[-1].priority:
                        postfix_list.append(stack.pop())
                stack.append(token)
        elif isinstance(token, Function):
            stack.append(token)
        elif isinstance(token, Constant):
            postfix_list.append(token)
        elif Parser.is_number(token):
            postfix_list.append(token)
        else:
            raise ValueError(f'name {token} is not defined')
    while stack:
        postfix_list.append(stack.pop())
    return postfix_list


def calculate(exp):
    stack = []
    parser = Parser()
    parsed_exp = parser.parse_expression(exp)
    polish = infix_to_postfix(parsed_exp)
    if all(isinstance(token, Operator) for token in polish):
        raise ValueError('not valid input')
    for token in polish:
        if isinstance(token, Operator) or isinstance(token, Function) or isinstance(token, Constant):
            if isinstance(token, Function) and len(polish) == 1:
                stack.append(token.func())
            elif isinstance(token, Function):
                x = stack.pop()
                if type(x) is list:
                    res = token.func(*x)
                else:
                    res = token.func(*[x])
                stack.append(res)
            elif isinstance(token, Constant):
                stack.append(token.func)
            elif not token.is_binary:
                x = stack.pop()
                stack.append(token.func(x))
            else:
                try:
                    y, x = stack.pop(), stack.pop()
                    stack.append(token.func(x, y))
                except Exception as e:
                    raise ValueError(f' binary operation must have two operands {e}')

        else:
            stack.append(float(token))
    return stack[0]
