def finding_elements(s):
    lis = []
    unit_num = ''
    unit_fun = ''
    s += ' '
    i = 0
    while i < len(s):

        if 96 < ord(s[i]) < 122:
            if unit_num:
                unit_num = verify_num(unit_num)
                lis.append(unit_num)
                unit_num = ''
            unit_fun += s[i]
            unit_fun = verify_pi_e(unit_fun, lis)

        elif (47 < ord(s[i]) < 58) or s[i] == '.':
            if unit_fun:
                lis.append(unit_fun)
                unit_fun = ''
            unit_num += s[i]

        else:
            if unit_num:
                unit_num = verify_num(unit_num)
                lis.append(unit_num)
                unit_num = ''
            if unit_fun:
                lis.append(unit_fun)
                unit_fun = ''
            lis.append(s[i])

        i += 1
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
        lis.append(2.718281828459045)
        return ''
    elif unit_func == 'pi':
        lis.append(3.141592653589793)
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
            if prior(lis[i + 1]) == 5 or lis[i + 1] == '(':
                lis.insert(i + 1, '*')
        elif lis[i] == ')':
            if lis[i + 1] == '(' or prior(lis[i + 1]) == 5:
                lis.insert(i + 1, '*')

        i += 1

    i = 0
    while i < len(lis) - 1:

        if prior(lis[i]) == 1 and prior(lis[i+1]) == 1:
            if lis[i] != lis[i+1]:
                lis[i] = '-'
            else:
                lis[i] = '+'
            del lis[i+1]
            continue

        elif type(lis[i]) == float:
            if (prior(lis[i + 1]) == 5 or lis[i + 1] == '(') and type(lis[i + 1]) != float:
                lis.insert(i + 1, '*')
        elif lis[i] == ')':
            if lis[i + 1] == '(' or prior(lis[i + 1]) == 5:
                lis.insert(i + 1, '*')

        elif (prior(lis[i]) == 2 or prior(lis[i]) == 3) and prior(lis[i+1]) == 1:
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


def prior(op):
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


def bin_operate(a, b, op):
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
        print('ERROR: arguments of function "' + s[i-1] + '" should be between hooks')
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
