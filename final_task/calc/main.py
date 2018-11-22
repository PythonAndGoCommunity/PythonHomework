import calc.functions as f

import argparse


def decide_expression(inp_s):
    # delete the spaces, add "(" to the beginning, and two spaces to the end and convert the string to the list
    s = list('(' + inp_s.replace(' ', '') + '  ')

    # bring the list to a convenient (element) type
    try:
        s = f.finding_elements(s)

        # print(s)

        steck_ops = []
        steck_nums = []

        i = 0

        # main cycle
        while i < len(s):
            f.verify(i, steck_nums, steck_ops, s)
            i += 1

        # print(steck_nums[0])
        return steck_nums[0]
    except:
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

    if z == True:
        print(decide_expression(inp_s))

