import math
import sys

STR_DIGITS = '0123456789'
STR_OPERATOR = '^*/%+-<=>!'
MATH_CONST = ['pi', 'e', 'tau', 'inf', 'nan']
ACCURACY = 1e-100
PREFIX_CONST = '#C'
PREFIX_FUNC = '#F'

PRIORITY_DICT = {
    '^': 5,
    '+-': 5,
    '*': 4,
    '/': 4,
    '//': 4,
    '%': 4,
    '+': 3,
    '-': 3,
    '<=': 2,
    '>=': 2,
    '<': 1,
    '>': 1,
    '==': 1,
    '!=': 1}
BOOL_DICT = {'True': True, 'False': False}
FUNCTION_DICT = {'abs': abs, 'pow': pow, 'round': round}


def stack_push(stack, token):
    buf_str = ''
    if token == '^' or token == '+-':
        for i in range(len(stack)):
            if stack[-1] == '(':
                break
            elif PRIORITY_DICT[token] < PRIORITY_DICT[stack[-1]]:
                buf_str += stack.pop() + ' '
            else:
                break
        stack.append(token)

    else:
        for i in range(len(stack)):
            if stack[-1] == '(':
                break
            elif PRIORITY_DICT[token] <= PRIORITY_DICT[stack[-1]]:
                buf_str += stack.pop() + ' '
            else:
                break
        stack.append(token)
    return buf_str


def shunting_yard(input_str):
    if len(input_str) == 0:
        raise Exception('empty input')
    stack = []
    output_str = ''
    func_buf = ''
    last_token = ''
    count_args = 1
    i = 0
    while i < len(input_str):
        token = input_str[i]
        if token == ' ':
            i += 1
            continue

        if ((token >= 'A') & (token <= 'Z')) \
                or ((token >= 'a') & (token <= 'z')):
            func_buf += token
            last_token = token
            i += 1
            continue
        elif func_buf:
            if token in STR_OPERATOR + ')':
                output_str += PREFIX_CONST + func_buf
                func_buf = ''
            elif token == '(':
                stack.append(PREFIX_FUNC + func_buf)
                func_buf = ''
                stack.append('(')
                last_token = token
                i += 1
                continue
            else:
                func_buf += token
                last_token = token
                i += 1
                continue

        if token in STR_DIGITS:
            output_str += token

        elif token == '.':
            output_str += '.'

        elif token == ',':
            count_args += 1
            output_str += ' '
            token = stack[-1]
            while token != '(':
                output_str += ' ' + stack.pop() + ' '
                token = stack[-1]

        elif token == '(':
            stack.append('(')

        elif token == ')':
            token = stack[-1]
            while token != '(':
                output_str += ' ' + stack.pop() + ' '
                if len(stack) != 0:
                    token = stack[-1]
                else:
                    raise Exception('unpaired brackets')
            else:
                stack.pop()
                if len(stack) != 0:
                    if PREFIX_FUNC in stack[-1]:
                        output_str += ' ' + str(count_args) + stack.pop()
                        count_args = 1
                token = ')'

        elif token in STR_OPERATOR:
            next_token = input_str[i + 1]
            output_str += ' '

            if (token == '-') & (last_token in STR_OPERATOR + '('):
                output_str += stack_push(stack, '+-')
            elif (token == '+') & (last_token in STR_OPERATOR):
                pass
            elif (token in ['<', '>', '!', '=']) & (next_token == '='):
                token += next_token
                output_str += stack_push(stack, token)
                i += 1
            elif token == '=':
                raise Exception('unknown operator: "="')
            elif (token == '/') & (next_token == '/'):
                token += next_token
                output_str += stack_push(stack, token)
                i += 1
            else:
                output_str += stack_push(stack, token)

        else:
            raise Exception('unknown operator: "' + token + '"')

        last_token = token
        i += 1

    if func_buf:
        output_str += PREFIX_CONST + func_buf

    while stack:
        token = stack.pop()
        if token == '(':
            raise Exception('unpaired brackets')
        output_str += ' ' + token

    return output_str


def pol(input_str):
    stack = []
    input_list = input_str.split(' ')
    for token in input_list:
        if token == '':
            continue
        elif token in PRIORITY_DICT:
            if token == '^':
                val2 = stack.pop()
                val1 = stack.pop()
                result = val1 ** val2
                if type(result) is complex:
                    return 'ERROR: negative number cannot be raised to a fractional power'
                stack.append(result)
            if token == '+-':
                stack[-1] = - stack[-1]
            if token == '*':
                val2 = stack.pop()
                stack.append(stack.pop() * val2)
            if token == '/':
                val2 = stack.pop()
                stack.append(stack.pop() / val2)
            if token == '//':
                val2 = stack.pop()
                stack.append(stack.pop() // val2)
            if token == '%':
                val2 = stack.pop()
                stack.append(stack.pop() % val2)
            if token == '+':
                val2 = stack.pop()
                stack.append(stack.pop() + val2)
            if token == '-':
                val2 = stack.pop()
                val1 = stack.pop()
                stack.append(val1 - val2)
            if token == '<=':
                val2 = stack.pop()
                stack.append(stack.pop() <= val2)
            if token == '>=':
                val2 = stack.pop()
                stack.append(stack.pop() >= val2)
            if token == '<':
                val2 = stack.pop()
                stack.append(stack.pop() < val2)
            if token == '>':
                val2 = stack.pop()
                stack.append(stack.pop() > val2)
            if token == '==':
                val2 = stack.pop()
                stack.append(stack.pop() == val2)
            if token == '!=':
                val2 = stack.pop()
                stack.append(stack.pop() != val2)
        elif token[2:] in BOOL_DICT:
            stack.append(BOOL_DICT[token[2:]])
        elif PREFIX_CONST in token:
            stack.append(getattr(math, token[2:]))
        elif PREFIX_FUNC in token:
            args_list = []
            for i in range(int(token[0])):
                args_list.append(stack.pop())
            if token[3:] in FUNCTION_DICT:
                x = FUNCTION_DICT[token[3:]](*args_list[::-1])
            else:
                x = getattr(math, token[3:])(*args_list[::-1])
            stack.append(x)
        else:
            stack.append(float(token))
    return stack.pop()


if __name__ == '__main__':
    print(pol(shunting_yard(sys.argv[1])))
