import calc.functions as f

import argparse


class Error(RuntimeError):
    pass


def num(s):
    if (ord(s) < 58 and ord(s) > 47) or s == '.':
        return 7
    else:
        return f.prior(s)


def decide_expression(inp_s):
    brackets = 0
    for j in range(0, len(inp_s)):
        if inp_s[j] == ' ' and j > 0 and j < len(inp_s) - 1:
            if num(inp_s[j - 1]) == num(inp_s[j + 1]) and (num(inp_s[j - 1]) > 1):
                print('ERROR: ...')
                exit(RuntimeError)
        if inp_s[j] == '(':
            brackets += 1
        elif inp_s[j] == ')':
            brackets -= 1
            if brackets < 0:
                print('ERROR: No balanced brackets')
                exit(Error)

    if brackets != 0:
        print('ERROR: No balanced brackets')
        exit(Error)

    s = list('(' + inp_s.replace(' ', '') + '  ')
    try:
        s = f.finding_elements(s)
        steck_ops = []
        steck_nums = []
        i = 0
        while i < len(s):
            f.verify(i, steck_nums, steck_ops, s)
            i += 1
        return steck_nums[0]
    except Error:
        print('ERROR: ...')
        exit(RuntimeError)


def main():
    parser = argparse.ArgumentParser(description='Takes only string')
    parser.add_argument('string')
    inp_s = parser.parse_args().string
    j = 0
    inp_s += ' '
    z = True
    while j < len(inp_s):
        if inp_s[j] == '!' and inp_s[j + 1] == '=':
            a = decide_expression(inp_s[:j])
            b = decide_expression(inp_s[j + 2:])
            print(a != b)
            z = False
            break
        elif inp_s[j] == '=' and inp_s[j + 1] == '=':
            a = decide_expression(inp_s[:j])
            b = decide_expression(inp_s[j + 2:])
            print(a == b)
            z = False
            break
        elif inp_s[j] == '<':
            if inp_s[j + 1] == '=':
                a = decide_expression(inp_s[:j])
                b = decide_expression(inp_s[j + 2:])
                print(a <= b)
                z = False
                break
            else:
                a = decide_expression(inp_s[:j])
                b = decide_expression(inp_s[j + 1:])
                print(a < b)
                z = False
                break
        elif inp_s[j] == '>':
            if inp_s[j + 1] == '=':
                a = decide_expression(inp_s[:j])
                b = decide_expression(inp_s[j + 2:])
                print(a >= b)
                z = False
                break
            else:
                a = decide_expression(inp_s[:j])
                b = decide_expression(inp_s[j + 1:])
                print(a > b)
                z = False
                break
        j += 1
    if z is True:
        print(decide_expression(inp_s))
