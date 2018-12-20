import argparse
import importlib
from string import ascii_letters, digits

# const variable
LIST_OPERATOR = ['+', '-', '*', '^', '/', '%', '<', '>', '=', '!']
LIST_DIGITS = list(digits)
LIST_LETTERS = list(ascii_letters)
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
# global variable dict, key: str module name, value: list containing fuction names from [key]
module_func_dict = {}
# Operator stack
stack_opr = []


def set_user_mod(modules=None):
    """set_user_mod(modules)

Initialize global variable module_func_dict

    """

    if not modules:
        return
    modules_list = [importlib.import_module(module) for module in modules]
    global module_func_dict
    module_func_dict = {module: dir(module) for module in modules_list}


def _stack_push(opr):
    """stack_push(opr)

This function is part of the shunting yard algorithm. Takes an operator and push it on the stack.
The operator pushes a stack of other operators.

"""

    global stack_opr
    buf = list()
    # right-associative operator
    if opr == '^' or opr == '+-':
        for opr2 in stack_opr[::-1]:
            if opr2 == '(':
                break
            elif PRIORITY_DICT[opr] < PRIORITY_DICT[opr2]:
                buf.extend([' ', stack_opr.pop()])
            else:
                break
        stack_opr.append(opr)

    # left-associative operator
    else:
        for opr2 in stack_opr[::-1]:
            if opr2 == '(':
                break
            elif PRIORITY_DICT[opr] <= PRIORITY_DICT[opr2]:
                buf.extend([' ', stack_opr.pop()])
            else:
                break
        stack_opr.append(opr)

    if opr != '+-':
        buf.append(' ')
    return buf


def _const_separator(const):
    """_const_separator(const)

Splits constants which are implicit multiplication. Example "pie" equal "pi*e". Constants are searched in the modules
defined in the variable module_func_dict.

"""
    global module_func_dict
    if const in BOOL_DICT:
        return const
    for module in module_func_dict:
        if const in module_func_dict[module]:
            return [const]
    else:
        # Recursion
        i = 0
        l_const = ''
        while i < len(const):
            l_const += const[i]
            r_const = const[i + 1:]
            for module in module_func_dict:
                if l_const in module_func_dict[module]:
                    return [l_const,  *_stack_push('*'), *_const_separator(r_const)]
            i += 1
        else:
            raise Exception('unknown constant {}'.format(const))


def postfix_translator(input_str):
    """postfix_translator(input_str)

The function converts a mathematical expression written in infix notation into postfix notation.
Implements an Shunting-yard algorithm

"""
    global module_func_dict
    global stack_opr

    if not input_str:
        raise Exception('empty input')

    output_list = list()
    func_buf = list()  # argument counter in function
    last_token = ''
    count_args = list()  # argument counter in function
    for i, token in enumerate(input_str):
        if token == ' ':
            output_list.append(' ')
            continue

        elif token in LIST_LETTERS or token == '_':
            if last_token == ')':
                output_list.extend(_stack_push('*'))
            if last_token in LIST_DIGITS:
                output_list.extend(_stack_push('*'))
            func_buf.append(token)

        elif token in LIST_DIGITS:
            if func_buf:
                func_buf.append(token)
            else:
                output_list.append(token)

        elif token == '.':
            output_list.append('.')

        elif token == ',':
            if count_args:
                count_args[-1] += 1
                output_list.append(' ')
                opr = stack_opr[-1]
                while opr != '(':
                    output_list.extend([' ', stack_opr.pop()])
                    opr = stack_opr[-1]
                output_list.append(' ')
            else:
                raise Exception('Using the symbol "," outside the function')

        elif token == '(':
            if func_buf:
                stack_opr.append(''.join(func_buf))
                count_args.append(1)
                func_buf = []
            elif last_token == ')' or last_token in LIST_DIGITS:
                output_list.extend(_stack_push('*'))
            stack_opr.append('(')

        elif token == ')':
            # function without argument
            if last_token == '(':
                count_args[-1] = 0
            if func_buf:
                output_list.extend(_const_separator(''.join(func_buf)))
                func_buf = []
            for opr in stack_opr[::-1]:
                if opr == '(':
                    stack_opr.pop()
                    break
                else:
                    output_list.extend([' ', stack_opr.pop()])
            else:
                raise Exception('unpaired brackets')
            # if function brackets
            if stack_opr:
                if stack_opr[-1] not in LIST_OPERATOR and stack_opr[-1] != '(':
                    output_list.extend([' ', stack_opr.pop(), '(', str(count_args.pop()), ')'])

        elif token in LIST_OPERATOR:
            if func_buf:
                output_list.extend(_const_separator(''.join(func_buf)))
                func_buf = []
            # unary operator
            if (token == '-') & (last_token in LIST_OPERATOR or last_token in ['', '(']):
                output_list.extend(_stack_push('+-'))
            elif (token == '+') & (last_token in LIST_OPERATOR or last_token == ''):
                pass
            # twice operator != <= >= ==
            elif token in ['=', '<', '>', '!']:
                if last_token in ['!=', '==', '<=', '>=', '!=']:
                    continue
                next_token = input_str[i + 1]
                if next_token == '=':
                    token += next_token
                    output_list.extend(_stack_push(token))
                elif token == '=':
                    raise Exception('unknown operator: "="')
                else:
                    output_list.extend(_stack_push(token))
            # twice operator //
            elif token == '/':
                if last_token == '//':
                    continue
                next_token = input_str[i + 1]
                if next_token == '/':
                    token = '//'
                    output_list.extend(_stack_push(token))
                else:
                    output_list.extend(_stack_push(token))
            # other operator
            else:
                output_list.extend(_stack_push(token))

        else:
            raise Exception('unknown operator: "{}"'.format(token))
        last_token = token

    if func_buf:
        output_list.extend(_const_separator(''.join(func_buf)))

    while stack_opr:
        token = stack_opr.pop()
        if token == '(':
            raise Exception('unpaired brackets')
        output_list.extend([' ', token])

    return ''.join(output_list)


def postfix_eval(input_str):
    """postfix_eval(input_str)

The function calculates the mathematical expression written in postfix notation.

    """

    global module_func_dict
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
        elif token in BOOL_DICT:
            stack.append(BOOL_DICT[token])
        # function
        elif '(' in token:
            pos = token.find('(')
            args_list = []
            for _ in range(int(token[pos+1:-1])):
                args_list.append(stack.pop())
            func_name = token[:pos]
            for module in module_func_dict:
                if func_name in module_func_dict[module]:
                    res = getattr(module, func_name)(*args_list[::-1])
                    break
            else:
                if func_name in FUNCTION_DICT:
                    res = FUNCTION_DICT[func_name](*args_list[::-1])
                else:
                    raise Exception('unknown function {}'.format(func_name))
            stack.append(res)
        # const
        elif token.isidentifier():
            for module in module_func_dict:
                if token in module_func_dict[module]:
                    stack.append(getattr(module, token))
                    break
        # number
        else:
            stack.append(float(token))
    if len(stack) > 1:
        raise Exception('invalid input')
    return stack.pop()


def main():
    """Entry point"""

    parser = argparse.ArgumentParser(add_help=True, description="Pure-python command-line calculator.")
    parser.add_argument("EXPRESSION", type=str, help="expression string to evaluate")
    parser.add_argument('-m', '--use-modules', dest='MODULE', type=str, nargs='+',
                        action='store', help="additional modules to use")
    args = parser.parse_args()
    if args.MODULE:
        args.MODULE.append('math')
    else:
        args.MODULE = ['math']
    try:
        set_user_mod(tuple(args.MODULE))
        print(postfix_eval(postfix_translator(args.EXPRESSION)))
    except Exception as err:
        print('ERROR:', err)


if __name__ == "__main__":
    main()
