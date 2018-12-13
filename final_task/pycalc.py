import math
import operator
import importlib.util
import argparse
import sys

OPERATORS = {'+': (2, operator.add), '-': (2, operator.sub),
             '*': (3, operator.mul), '/': (3, operator.truediv),
             '^': (4, operator.pow), '//': (3, operator.floordiv),
             '%': (3, operator.mod), '<': (1, operator.lt),
             '<=': (1, operator.le), '>': (1, operator.gt),
             '!=': (1, operator.ne), '>=': (1, operator.ge),
             '==': (1, operator.eq), '?': (4, operator.neg)}

STLO = {'True': True, 'False': False}
FUNCTION = {'round': round, 'abs': abs, 'pow': pow}
STNUMBER = '1234567890.'
STBUK = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_'
STOP = '<+->/!=*^%'

version = "1.2.1"
global module

def createparser():
    parser = argparse.ArgumentParser(
        prog='''pycalc''',
        description='''A program to calculate complex mathematical expressions 
        with support for custom libraries.''',
        epilog='''(c) Nick Dubovik 2018. The author of the program, as always,does not take any responsibility for 
        anything.''',
        add_help=False)
    parent_group = parser.add_argument_group(title='Optional arguments')
    parent_group.add_argument('--help', '-h', action='help', help='Help')
    parser.add_argument('--mod', '-m', default='math', help='Additional modules to use',
                        metavar='MODULE')
    parser.add_argument('string', type=str, default='', help='Expression string to evaluate',
                        metavar='EXPRESSION')
    # subparsers = parser.add_subparsers (dest = 'command',
    #        title = 'possible program',
    #        description = 'Commands that should be %(prog)s')
    parent_group.add_argument('--version', action='version', help='Show the version number',
                              version='%(prog)s {}'.format(version))
    return parser


def check_module(module_name):
    # Checks if the module can be imported without actually importing it
    module_spec = importlib.util.find_spec(module_name)
    if module_spec is None:
        # print('Module: {} not found'.format(module_name))
        return None
    else:
        # print('Module: {} can be imported!'.format(module_name))
        return module_spec


def import_module_from_spec(module_spec):
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def sum(module, sst):
    # Reading and token allocation--------------------------------------------------------------------
    def parse(sst):
        if len(sst) == 0:
            raise Exception('Empty expression.')
        pr = 0
        lev = 0
        last_op = ''
        for j, s in enumerate(sst):
            if s == ' ':
                if sst[j - 1] in '/*%^><=' and sst[j + 1] in '/*%^><=':
                    raise Exception('Пробел между знаками')
                if sst[j - 1] in STNUMBER and sst[j + 1] in STNUMBER:
                    raise Exception('Пробел')
        st = sst.replace(" ", "")
        if st[0] in '+-':
            st = "0" + st
        n = len(st)
        i = 0
        while i < n:
            if st[i] in STNUMBER:
                last_op = ''
                number = ''
                # if st[i] == '.':
                # number += '0'
                while st[i] in STNUMBER:
                    number += st[i]
                    i = i + 1
                    if i >= n:
                        break
                if i >= n:
                    yield (float(number))
                    break
                elif i < n and (st[i] in STOP or st[i] == ')' or st[i] == ','):
                    yield (float(number))
                elif i < n and st[i] in STBUK or st[i] == '(':
                    yield float(number)
                    yield '*'

            if st[i] in STOP:
                if st[0] in '*/%^><=!':
                    raise Exception('No arguments befor operator')
                op = ''
                while st[i] in STOP:
                    op += st[i]
                    i = i + 1
                    if op in '-+^%*':
                        break
                    elif i < n and op in '-+^%*/><=' and st[i] in '+-':
                        break
                    if i >= n:
                        break
                if last_op != '':
                    if op == '-':
                        op = "?"
                        yield "?"
                        last_op = op
                    elif op == '+':
                        last_op = op
                else:
                    if i >= n:
                        raise Exception('The operator has not got arguments.')
                    yield op
                    last_op = op

            if st[i] in STBUK:
                last_op = ''
                func = ''
                while st[i] in STBUK or st[i] in STNUMBER:
                    func += st[i]
                    i = i + 1
                    if (i < n and (hasattr(math, func) or hasattr(module, func)) and (
                            st[i] == '(' or st[i] in STBUK)) or i >= n or func in STLO:
                        break
                if i >= n:
                    if hasattr(math, func) or hasattr(module, func):  # написать
                        cc = '$' + func + '@'
                        yield cc
                    elif func in STLO:
                        logic = ''
                        logic += '$' + func + '#'
                        yield logic
                    else:
                        raise Exception(func + ' is not in the library.')
                else:
                    if st[i] == '(' and (hasattr(math, func) or hasattr(module, func) or func in FUNCTION):  # function
                        f = ''
                        # к-number of '()',z-number of ','
                        k = 0
                        z = 0
                        j = i
                        while k != 0 or j < n:
                            if st[j] == ')':
                                k = k - 1
                            elif st[j] == '(':
                                k = k + 1
                            elif st[j] == ',' and k == 1:
                                z = z + 1
                            j = j + 1
                            if j >= n or k == 0:
                                break
                        zz = str(z)
                        f += '$' + zz + func + '&'  # function
                        yield f

                    elif hasattr(math, func) or hasattr(module, func):
                        const = ''
                        const += '$' + func + '@'  # const
                        if st[i] in STBUK or st[i] in STNUMBER:
                            yield const
                            yield '*'
                        else:
                            yield const

                    elif func in STLO:
                        logic = ''
                        logic += '$' + func + '#'  # const
                        if st[i] in STBUK or st[i] in STNUMBER:
                            yield logic
                            yield '*'
                        else:
                            yield logic
                    else:
                        raise Exception(func + ' is not in the library.')
                if i >= n:
                    break

            if st[i] in '()':
                if st[i] == '(':
                    lev = lev + 1
                    last_op = '('
                elif st[i] == ')':
                    pr = pr + 1
                    last_op = ''
                i = i + 1
                if i < n and st[i - 1] == ')' and (st[i] in STNUMBER or st[i] in STBUK or st[i] == '('):
                    yield st[i - 1]
                    yield '*'
                else:
                    yield st[i - 1]
                if i >= n:
                    break

            if st[i] == ',':
                last_op = ','
                i = i + 1
                yield st[i - 1]
                if i >= n:
                    break
        if pr != lev:
            raise Exception('Unequal number of brackets')

    # conversion to Polish notation------------------------------------------------------------------------------

    def shunting_yard(parsed_formula):
        stack = []
        for token in parsed_formula:

            if type(token) is str and token[0] == '$' and token[-1] == '&':
                stack.append(token)  # function

            elif type(token) is str and token[0] == '$' and token[-1] == '@':
                mcon = token.replace('$', '').replace('@', '')
                zz = getattr(math, mcon)
                yield float(zz)  # const

            elif type(token) is str and token[0] == '$' and token[-1] == '#':
                mlo = token.replace('$', '').replace('#', '')
                yield STLO[mlo]  # logic

            elif token in OPERATORS:
                if token == '^' or token == '?':
                    while stack and stack[-1] != "(" and OPERATORS[token][0] < OPERATORS[stack[-1]][0]:  # think
                        yield stack.pop()
                else:
                    while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                        yield stack.pop()
                stack.append(token)

            elif token == ',':
                while stack:
                    if stack[-1] == '(':
                        break
                    yield stack.pop()

            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
                if stack:
                    yy = stack[-1]
                    if type(yy) is str and yy[0] == '$' and yy[-1] == '&':
                        yield stack.pop()

            elif token == "(":
                stack.append(token)

            elif type(token) is float:
                yield token

        while stack:
            yield stack.pop()

    # calculating Polish notation------------------------------------------------------------------------------

    def calculation(polish):
        stack = []
        for token in polish:
            if token in OPERATORS:
                if token == '?':
                    x = stack.pop()
                    stack.append(OPERATORS[token][1](x))
                else:
                    y, x = stack.pop(), stack.pop()
                    stack.append(OPERATORS[token][1](x, y))

            elif type(token) is str and token[0] == '$' and token[-1] == '&':
                mfun = token.replace('$', '').replace('&', '')
                kk = ''
                for s in mfun:
                    if s in STNUMBER:
                        kk += s
                    else:
                        break
                k = int(kk)
                # k-number of ',' k+1-number of arguments for function
                mmfun = mfun.lstrip(kk)
                x = []  # list of arguments for function
                for l in range(k + 1):
                    y = stack.pop()
                    # if type(y) is float:
                    x.append(y)
                if hasattr(module, mmfun):
                    z = getattr(module, mmfun)
                    stack.append(z(*x[::-1]))
                elif hasattr(math, mmfun):
                    z = getattr(math, mmfun)
                    stack.append(z(*x[::-1]))
                elif mmfun in FUNCTION:
                    g = FUNCTION[mmfun](*x[::-1])
                    stack.append(g)
                else:
                    raise Exception('The function is not in the library.')
                    # print(stack)
            else:
                stack.append(token)

        return stack[0]

    return calculation(shunting_yard(parse(st)))


# main------------------------------------------------------------------------------------

if __name__ == "__main__":
    parser = createparser()
    namespace = parser.parse_args(sys.argv[1:])
    # print(namespace)
    try:
        lib = namespace.mod
        # lib is connected library
        st = namespace.string
        module_spec = check_module(lib)
        if module_spec:
            module = import_module_from_spec(module_spec)
        print(sum(module, st))  # Output result
    except Exception as error:
        print('ERROR: ' + repr(error))
