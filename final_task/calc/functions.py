from calc.math_functions import decide_func as d_f

def finding_elements(s):
    """Select the individual elements of our expression: various operations, function names, numbers.
    Lead to the completed form for processing. """

    #adding constantes
    e = 2.718281828459045
    pi = 3.141592653589793
    tau = 6.283185307179586
    pie = 8.539734222673566

    num_v = ''
    fun_v = ''
    i = 0

    def del_els(i, n):
        """ Removes list members that have become part of a single item.
        ['a', 'b', 's'] -> ['abs'], n = 3, s[i] = 's' """
        for j in range(n-1):
            del s[i-1]
            i -= 1
        return i+1


    while i < len(s)-1:

        if (ord(s[i]) < 58 and ord(s[i]) > 47) or s[i] == '.':
            # the sequence of numbers and points is separated into one line

            num_v += s[i]
        else:
            if num_v:

                i -= 1

                try:# try to convert received string to float
                    s[i] = float(num_v)
                except:
                    s[i] = num_v
                    print('ERROR: ', num_v + ' --- incorrect value')
                    exit(ValueError)

                i = del_els(i, len(num_v))
                num_v = ''

        if ord(s[i]) > 96 and ord(s[i]) < 122:
            # the sequence of letter is separated into the one line

            fun_v += s[i]
        else:
            if fun_v:
                if fun_v == 'e':
                    s[i-1] = e
                elif fun_v == 'pi':
                    s[i-1] = pi
                elif fun_v == 'tau':
                    s[i-1] = tau
                elif fun_v == 'epi' or fun_v == 'pie':
                    s[i-1] = pie
                else:
                    s[i-1] = fun_v # received string include as one of element of list
                i = del_els(i-1, len(fun_v))
                fun_v = ''
                
        # envisage cases where an element can consist of two
        if s[i] == '/' and s[i+1] == '/':
            s[i] = '//'
            del s[i + 1]

        elif s[i] == '+':
            if s[i+1] == '-':
                s[i] = '-'
                del s[i+1]
                i -= 1
            elif s[i+1] == '+':
                del s[i+1]
                i -= 1

        elif s[i] == '-':

            if s[i+1] == '-':
                s[i] = '+'
                del s[i+1]
                i -= 1
            elif s[i+1] == '+':
                del s[i+1]
                i -= 1
            elif s[i - 1] == '/' or s[i - 1] == '^':
                s.insert(i, '(')
                s.insert(i+5, ')')



        i += 1



    s = s[:-1] # del one of two spaces in the end
    s[-1] = ')' # last space replace to ")"
    s = finding_func_with_nums(s) # envisage functions with number in name
    s = adding_multiply(s) # envisage unary minuses and multiply without char "*"

    return s

def adding_multiply(s):
    """Add * between together part for multiply"""
    i = 0


    while i < len(s)-1: # find potential situation
        if type(s[i]) == float:
            if prior(s[i+1]) == 5 or s[i+1] == '(':
                s.insert(i+1, '*')
        elif s[i] == ')':
            if s[i+1] == '(' or prior(s[i+1]) == 5 or type(s[i+1]) == float:
                s.insert(i+1, '*')

        i += 1

    return s



def prior(op):
    """distribute priorities to possible elements of an expression"""
    if op == '(' or op == ')':
        return 0

    elif op == '+' or op == '-':
        return 1

    elif op == '/' or op == '*' or op == '//' or op == '%':
        return 2

    #elif op == '//' or op == '%':  error in test '100/3%2^2'
    #   return 3

    elif op == '^':
        return 4

    elif op == ',':
        return 6

    else:
        return 5




def bin_operate(a, b, op):
    """determinate binary operates"""
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
            return a/b
        else:
            return 'divide by zero'

    elif op == '//':
        if b != 0:
            return a//b
        else:
            return 'divide by zero'


def finding_func_with_nums(s):
    """find functions with numbers in name"""
    i = 0

    while i < len(s):
        if s[i] == 'expm' and s[i+1] == 1.0:
            s[i] = 'expm1'
            del s[i+1]

        elif s[i] == 'log':
            if s[i+1] == 10.0:
                s[i] = 'log10'
                del s[i+1]
            elif s[i+1] == 2.0:
                s[i] = 'log2'
                del s[i+1]
            elif s[i+1] == 1.0 and s[i+2] == 'p':
                s[i] = 'log1p'
                del s[i+1]
                del s[i+1]

        elif s[i] == 'atan' and s[i+1] == 2.0:
            s[i] = 'atan2'
            del s[i+1]

        i += 1

    return s

def selection(i, s):
    """select expression for function"""
    hooks = 1
    i = i+1
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


def get_args(s):
    """select arguments for function"""
    args = []
    h = 0
    arg = ['(']

    for i in s[1:-1]:
        if i == ',' and h == 0:
            arg.append(')')
            args.append(arg)
            arg = ['(']
        else:
            arg.append(i)
            if i == '(':
                h += 1
            elif i == ')':
                h -= 1

    arg.append(')')
    if len(arg) > 2:
        args.append(arg)

    return args

def deciding_args(args):
    """decide values of arguments"""
    ready_args = []
    for s in args:

        steck_nums = []
        steck_ops = []
        i = 0
        while i < len(s):
            verify(i, steck_nums, steck_ops, s)
            i += 1
        ready_args.append(steck_nums[0])

    return ready_args



def deciding_function(i, s):
    """decide and find value of the function """
    line = selection(i, s)
    args = get_args(line)
    ready_args = deciding_args(args)
    d_f(s, i, ready_args)




def verify(i, steck_nums, steck_ops, s):
    """verify element, and perform necessary actions"""

    if type(s[i]) == float:
        steck_nums.append(s[i])

    elif s[i] == '(':
        steck_ops.append('(')
        if s[i+1] == '+' or s[i+1] == '-':
            steck_nums.append(0)

    elif s[i] == ')':
        if steck_ops[-1] == '(':
            del steck_ops[-1]
        else:
            steck_nums[-2] = bin_operate(steck_nums[-2], steck_nums[-1], steck_ops[-1])
            del steck_nums[-1]
            del steck_ops[-1]
            verify(i, steck_nums, steck_ops, s)

    elif prior(s[i]) == 5:
        deciding_function(i, s)
        verify(i, steck_nums, steck_ops, s)


    elif prior(s[i]) <= prior(steck_ops[-1]):
        if s[i] == '^' and steck_ops[-1] == '^':
            steck_ops.append(s[i])
        else:
            steck_nums[-2] = bin_operate(steck_nums[-2], steck_nums[-1], steck_ops[-1])
            del steck_nums[-1]
            del steck_ops[-1]
            verify(i, steck_nums, steck_ops, s)


    elif prior(s[i]) > prior(steck_ops[-1]):
        steck_ops.append(s[i])
