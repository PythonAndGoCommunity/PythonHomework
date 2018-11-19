import argparse
import importlib
from string import ascii_letters, digits

LIST_OPERATOR = ['+', '-', '*', '^', '/', '%', '<', '>', '=', '!']
LIST_DIGITS = list(digits)
LIST_LETTERS = list(ascii_letters)
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


def stack_push(stack, opr):
    """stack_push(stack, opr)

This function is part of the shunting yard algorithm"""

    buf_str = ''
    if opr == '^' or opr == '+-':
        for opr2 in stack[::-1]:
            if opr2 == '(':
                break
            elif PRIORITY_DICT[opr] < PRIORITY_DICT[opr2]:
                buf_str += stack.pop() + ' '
            else:
                break
        stack.append(opr)

    else:
        for opr2 in stack[::-1]:
            if opr2 == '(':
                break
            elif PRIORITY_DICT[opr] <= PRIORITY_DICT[opr2]:
                buf_str += stack.pop() + ' '
            else:
                break
        stack.append(opr)
    return buf_str


def shunting_yard_alg(input_str):
    """shunting_yard_alg(input_str)

The function converts a mathematical expression written in infix notation into postfix notation."""

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
            output_str += ' '
            token = last_token

        elif token in LIST_LETTERS \
                or token == '_':
            if last_token in LIST_DIGITS or last_token == ')':
                output_str += ' '
                output_str += stack_push(stack, '*')
            func_buf += token

        elif token in LIST_DIGITS:
            if func_buf:
                func_buf += token
            else:
                output_str += token

        elif token == '.':
            output_str += '.'

        elif token == ',':
            count_args += 1
            output_str += ' '
            opr = stack[-1]
            while opr != '(':
                output_str += ' ' + stack.pop() + ' '
                opr = stack[-1]

        elif token == '(':
            if func_buf:
                stack.append(PREFIX_FUNC + func_buf)
                func_buf = ''
            elif last_token == ')' or last_token in LIST_DIGITS:
                output_str += ' '
                output_str += stack_push(stack, '*')
            stack.append('(')

        elif token == ')':
            if last_token == '(':
                count_args = 0
            if func_buf:
                output_str += ' ' + PREFIX_CONST + func_buf
                func_buf = ''
            if stack:
                opr = stack[-1]
                while opr != '(':
                    output_str += ' ' + stack.pop() + ' '
                    if len(stack) != 0:
                        opr = stack[-1]
                    else:
                        raise Exception('unpaired brackets')
                stack.pop()
            else:
                raise Exception('unpaired brackets')
            if stack:
                if PREFIX_FUNC in stack[-1]:
                    output_str += ' ' + str(count_args) + stack.pop()
                    count_args = 1

        elif token in LIST_OPERATOR:
            if func_buf:
                output_str += PREFIX_CONST + func_buf
                func_buf = ''

            next_token = input_str[i + 1]
            output_str += ' '
            if (token == '-') & (last_token in LIST_OPERATOR or last_token in ['', '(']):
                output_str += stack_push(stack, '+-')
            elif (token == '+') & (last_token in LIST_OPERATOR):
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
            raise Exception('unknown operator: "{}"'.format(token))

        last_token = token
        i += 1

    if func_buf:
        output_str += PREFIX_CONST + func_buf

    while stack:
        token = stack.pop()
        if token == '(':
            raise Exception('unpaired brackets')
        output_str += ' ' + token
    print(output_str)
    return output_str


def postfix_eval(input_str, modules=tuple()):
    """postfix_eval(input_str)

The function calculates the mathematical expression written in postfix notation.
    """

    module_func_dict = {module: dir(module) for module in modules}
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
            pos = token.find(PREFIX_CONST)
            const_name = token[pos + len(PREFIX_CONST):]
            for module in module_func_dict:
                if const_name in module_func_dict[module]:
                    stack.append(getattr(module, const_name))
                    break
            else:
                raise Exception('unknown constant {}'.format(const_name))
        elif PREFIX_FUNC in token:
            pos = token.find(PREFIX_FUNC)
            args_list = []
            for i in range(int(token[:pos])):
                args_list.append(stack.pop())
            func_name = token[pos + len(PREFIX_FUNC):]
            for module in module_func_dict:
                if func_name in module_func_dict[module]:
                    res = getattr(module, token[3:])(*args_list[::-1])
                    break
            else:
                if func_name in FUNCTION_DICT:
                    res = FUNCTION_DICT[func_name](*args_list[::-1])
                else:
                    raise Exception('unknown function {}'.format(func_name))
            stack.append(res)
        else:
            stack.append(float(token))
    if len(stack) > 1:
        raise Exception('invalid input')
    return stack.pop()


def main():
    """Entry point"""

    parser = argparse.ArgumentParser(add_help=True, description="Pure-python command-line calculator.")
    parser.add_argument("EXPRESSION", type=str,  help="expression string to evaluate")
    parser.add_argument('-m', '--use-modules', dest='MODULE', type=str, nargs='+',
                        action='store', help="additional modules to use")
    args = parser.parse_args()
    if args.MODULE:
        args.MODULE.append('math')
    else:
        args.MODULE = ['math']
    modules = [importlib.import_module(module) for module in args.MODULE]
    try:
        print(postfix_eval(shunting_yard_alg(args.EXPRESSION), modules))
    except Exception as err:
        print('ERROR:', err)


if __name__ == "__main__":
    main()
