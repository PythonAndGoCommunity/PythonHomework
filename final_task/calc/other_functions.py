from math import pi, e, tau


def finding_elements(s):
    lis = []
    ord_a = 97
    ord_z = 122
    ord_0 = 48
    ord_9 = 57
    unit_num = ''
    unit_fun = ''
    s += ' '
    for element in s:

        if ord_a <= ord(element) <= ord_z:
            if unit_num:
                unit_num = verify_num(unit_num)
                lis.append(unit_num)
                unit_num = ''
            unit_fun += element
            unit_fun = verify_pi_e(unit_fun, lis)

        elif (ord_0 <= ord(element) <= ord_9) or element == '.':
            if unit_fun:
                lis.append(unit_fun)
                unit_fun = ''
            unit_num += element

        else:
            if unit_num:
                unit_num = verify_num(unit_num)
                lis.append(unit_num)
                unit_num = ''
            if unit_fun:
                lis.append(unit_fun)
                unit_fun = ''
            lis.append(element)

    return lis


def verify_num(str_num):
    try:
        float_num = float(str_num)
        return float_num
    except Exception:
        print('ERROR: incorrect value "' + str_num + '"')
        exit()


def verify_pi_e(unit_func, lis):
    if unit_func == 'e':
        lis.append(e)
        return ''
    elif unit_func == 'pi':
        lis.append(pi)
        return ''
    elif unit_func == 'tau':
        lis.append(tau)
        return ''
    else:
        return unit_func


def additions(lis):
    i = 0
    while i < len(lis)-1:
        if lis[i] == '/' and lis[i+1] == '/':
            lis[i] = '//'
            del lis[i+1]

        elif lis[i] == 'expm' and lis[i+1] == 1:
            lis[i] = 'expm1'
            del lis[i+1]

        elif lis[i] == 'atan' and lis[i+1] == 2:
            lis[i] = 'atan2'
            del lis[i+1]

        elif lis[i] == 'log':
            if lis[i+1] == 10:
                lis[i] = 'log10'
                del lis[i+1]
            elif lis[i+1] == 2:
                lis[i] = 'log2'
                del lis[i+1]

        elif lis[i] == '=' and lis[i+1] != '=':
            del lis[i]
            lis[i-1] += '='
            continue

        elif type(lis[i]) == float:
            if get_prior(lis[i + 1]) == 5 or lis[i + 1] == '(':
                lis.insert(i + 1, '*')
        elif lis[i] == ')':
            if lis[i + 1] == '(' or get_prior(lis[i + 1]) == 5:
                lis.insert(i + 1, '*')

        i += 1

    i = 0
    while i < len(lis) - 1:

        if get_prior(lis[i]) == 1 and get_prior(lis[i+1]) == 1:
            if lis[i] != lis[i+1]:
                lis[i] = '-'
            else:
                lis[i] = '+'
            del lis[i+1]
            continue

        elif type(lis[i]) == float:
            if (get_prior(lis[i + 1]) == 5 or lis[i + 1] == '(') and type(lis[i + 1]) != float:
                lis.insert(i + 1, '*')
        elif lis[i] == ')':
            if lis[i + 1] == '(' or get_prior(lis[i + 1]) == 5:
                lis.insert(i + 1, '*')

        elif (get_prior(lis[i]) == 2 or get_prior(lis[i]) == 3) and get_prior(lis[i+1]) == 1:
            del lis[i+1]
            lis[i+1] *= -1
            continue

        elif lis[i] == ' ':
            del lis[i]
            continue

        if lis[i+1] == ' ':
            del lis[i+1]
            continue

        i += 1

    return lis


def get_prior(op):
    four_4 = [',', ' ', '<', '>', '=', '!', '>=', '<=', '==', '!=']
    if op == '(' or op == ')':
        return 0
    elif op == '+' or op == '-':
        return 1
    elif op == '/' or op == '*' or op == '//' or op == '%':
        return 2
    elif op == '^':
        return 3
    elif op in four_4:
        return 4
    else:
        return 5


def perform_bin_operate(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '%':
        return a % b
    elif op == '^':
        return a ** b
    elif op == '/':
        if b != 0:
            return a / b
        else:
            print('ERROR: divide by zero')
            exit()
    elif op == '//':
        if b != 0:
            return a // b
        else:
            print('ERROR: divide by zero')
            exit()
    else:
        print('ERROR: unknown operator "' + op + '"')
        exit()


def decide_function(i, s):

    line = get_line_args(i, s)
    args = get_args(line)
    return args


def get_line_args(i, s):
    hooks = 1
    i = i + 1
    if s[i] != '(':
        print('ERROR: arguments of function "' + str(s[i-1]) + '" should be between hooks')
        exit()
    line = [s[i]]
    del s[i]

    while hooks != 0 and i < len(s):
        if s[i] == '(':
            hooks += 1
        elif s[i] == ')':
            hooks -= 1
        line.append(s[i])
        del s[i]

    return line


def get_args(line):

    args = []
    h = 0
    arg = []

    for i in line[1:-1]:
        if i == ',' and h == 0:
            args.append(arg)
            arg = []
        else:
            arg.append(i)
            if i == '(':
                h += 1
            elif i == ')':
                h -= 1
    if arg:
        args.append(arg)
    return args
