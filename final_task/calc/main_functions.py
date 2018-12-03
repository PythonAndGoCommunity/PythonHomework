import calc.other_functions as o_f
from calc.math_functions import decide_func


def reduction_expression(s):

    lis = o_f.finding_elements(s)
    lis = o_f.additions(lis)
    return lis


def compare(lis):
    i = 0
    while i < len(lis)-1:
        if lis[i] == '==':
            a, b = cut(i, lis)
            return a == b
        elif lis[i] == '<=':
            a, b = cut(i, lis)
            return a <= b
        elif lis[i] == '>=':
            a, b = cut(i, lis)
            return a >= b
        elif lis[i] == '!=':
            a, b = cut(i, lis)
            return a != b
        elif lis[i] == '>':
            a, b = cut(i, lis)
            return a > b
        elif lis[i] == '<':
            a, b = cut(i, lis)
            return a < b

        i += 1

    return decide_expression(lis)


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
        exit()

    return st_nums[0]


def verify(s, i, st_nums, st_ops):

    if type(s[i]) == float:
        st_nums.append(s[i])

    elif s[i] == '(':
        st_ops.append('(')
        if o_f.prior(s[i+1]) == 1:
            st_nums.append(0)

    elif s[i] == ')':
        if st_ops[-1] == '(':
            del st_ops[-1]
        else:
            try:
                st_nums[-2] = o_f.bin_operate(st_nums[-2], st_nums[-1], st_ops[-1])
            except Exception:
                print('ERROR: not necessary element')
                exit()
            del st_ops[-1]
            del st_nums[-1]
            verify(s, i, st_nums, st_ops)

    elif o_f.prior(s[i]) == 5:
        args = o_f.decide_function(i, s)
        ready_args = decide_args(args)
        s[i] = decide_func(s[i], ready_args)
        verify(s, i, st_nums, st_ops)

    elif o_f.prior(s[i]) <= o_f.prior(st_ops[-1]):
        if s[i] == '^' and st_ops[-1] == '^':
            st_ops.append(s[i])
        else:
            try:
                st_nums[-2] = o_f.bin_operate(st_nums[-2], st_nums[-1], st_ops[-1])
            except Exception:
                print('ERROR: not necessary element')
                exit()
            del st_nums[-1]
            del st_ops[-1]
            verify(s, i, st_nums, st_ops)

    elif o_f.prior(s[i]) > o_f.prior(st_ops[-1]):
        st_ops.append(s[i])


def decide_args(args):
    ready_args = []
    for s in args:
        ready_args.append(decide_expression(s))

    return ready_args
