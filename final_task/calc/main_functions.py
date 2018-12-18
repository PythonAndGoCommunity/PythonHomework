from calc import other_functions
from calc.math_functions import decide_func


class ExpressionError(Exception):
    pass


def reduction_expression(string):
    lis = other_functions.finding_elements(string)
    lis = other_functions.additions(lis)
    return lis


def check_compared(composition):
    i = 0
    while i < len(composition)-1:
        if composition[i] == '==':
            a, b = cut(i, composition)
            return a == b
        elif composition[i] == '<=':
            a, b = cut(i, composition)
            return a <= b
        elif composition[i] == '>=':
            a, b = cut(i, composition)
            return a >= b
        elif composition[i] == '!=':
            a, b = cut(i, composition)
            return a != b
        elif composition[i] == '>':
            a, b = cut(i, composition)
            return a > b
        elif composition[i] == '<':
            a, b = cut(i, composition)
            return a < b

        i += 1

    return decide_expression(composition)


def cut(i, lis):
    a = decide_expression(lis[:i])
    b = decide_expression(lis[i+1:])
    return a, b


def decide_expression(s):
    s.insert(0, '(')
    s.append(')')
    st_nums = []
    st_ops = []
    i = 0

    while i < len(s):
        verify(s, i, st_nums, st_ops)
        i += 1

    if len(st_nums) > 1 or len(st_ops):
        print('ERROR: not necessary operation')
        raise ExpressionError

    return st_nums[0]


def verify(string, index, st_nums, st_ops):
    if type(string[index]) == float:
        st_nums.append(string[index])

    elif string[index] == '(':
        st_ops.append('(')
        if other_functions.get_prior(string[index+1]) == 1:
            st_nums.append(0)

    elif string[index] == ')':
        if st_ops[-1] == '(':
            del st_ops[-1]
        else:
            try:
                st_nums[-2] = other_functions.perform_bin_operate(st_nums[-2], st_nums[-1], st_ops[-1])
            except Exception:
                print('ERROR: not necessary element')
                raise ExpressionError
            del st_ops[-1]
            del st_nums[-1]
            verify(string, index, st_nums, st_ops)

    elif other_functions.get_prior(string[index]) == 5:
        args = other_functions.decide_function(index, string)
        ready_args = decide_args(args)
        string[index] = decide_func(string[index], ready_args)
        verify(string, index, st_nums, st_ops)

    elif other_functions.get_prior(string[index]) <= other_functions.get_prior(st_ops[-1]):
        if string[index] == '^' and st_ops[-1] == '^':
            st_ops.append(string[index])
        else:
            try:
                st_nums[-2] = other_functions.perform_bin_operate(st_nums[-2], st_nums[-1], st_ops[-1])
            except Exception:
                print('ERROR: not necessary element')
                raise ExpressionError
            del st_nums[-1]
            del st_ops[-1]
            verify(string, index, st_nums, st_ops)

    elif other_functions.get_prior(string[index]) > other_functions.get_prior(st_ops[-1]):
        st_ops.append(string[index])


def decide_args(args):
    ready_args = []
    for s in args:
        ready_args.append(decide_expression(s))

    return ready_args
