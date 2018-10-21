import re


binary_operations = {
    "+": 0,
    "-": 0,
    "*": 1,
    "/": 1,
    "//": 1,
    "%": 1,
    "^": 2,
}


ops_list = dict(log=1, log10=1, abs=1, sqrt=1, sin=1, asin=1, cos=1, acos=1, hypot=1, tan=1, atan=1, atan2=1, ceil=1,
                copysign=1, fabs=1, factorial=1, floor=1, fmod=1, frexp=1, ldexp=1, fsum=1, isfinite=1, isinf=1,
                isnan=1, modf=1, trunc=1, exp=1, expm1=1, log1p=1, log2=1, pow=1, degrees=1, radians=1, cosh=1, sinh=1,
                tanh=1, acosh=1, asinh=1, atanh=1, erf=1, erfc=1, gamma=1, lgamma=1, pi=1, e=1, inv=0, gcd=1, isclose=1,
                isdexp=1, tau=1, inf=1, nan=1,
                )


def correct_expression(expression):
    re_expr = re.findall('log10|log2|log1p|expm1|atan2|\//|\d+\.\d+|\d+|\W|\w+',expression)
    i = 0
    _len = lambda x: len(x)
    for i in range(_len(re_expr)):
        if re_expr[i].isdigit() and re_expr[i + 1] == '(':
            re_expr.insert(i + 1, '*')
            print('a')
        elif re_expr[i].isdigit() and re_expr[i + 1] in ops_list:
            re_expr.insert(i + 1, '*')
            print('q')
            print(re_expr[i+2])
        elif re_expr[i] == ')' and re_expr[i + 1][0].isdigit():
            re_expr.insert(i + 1, '*')
            i += 1
            print('b')
        if i + 2 >= _len(re_expr):
            break
    return re_expr


def calc(expression):
    stack = []
    expression = to_postfix(expression)
    for i in expression:
        if i.isnumeric():
            stack.append(i)
        elif i in binary_operations:
            b = int(stack.pop())
            a = int(stack.pop())
            if i == '+':
                stack.append(a + b)
            if i == '-':
                stack.append(a - b)
            if i == '*':
                stack.append(a * b)
            if i == '/':
                stack.append(a / b)
            if i == '//':
                stack.append(a // b)
            if i == '%':
                stack.append(a % b)
            if i == '^':
                stack.append(a ** b)
    return stack.pop()


def to_postfix(expression):
    res = []
    stack = []
    for i in correct_expression(expression):
        if i.isnumeric():
            res.append(i)
        elif i == '(':
            stack.append(i)
        elif i == ')':
            while stack[-1] != '(':
                res.append(stack.pop())
            stack.pop()
        elif i in binary_operations:
            if stack and stack[-1] in binary_operations and binary_operations[stack[-1]] >= binary_operations[i]:
                while stack and binary_operations[stack[-1]] >= binary_operations[i]:
                    res.append(stack.pop())
                stack.append(i)
            else:
                stack.append(i)
    for i in reversed(stack):
        res.append(i)
    return res


a = "2^3+2"
print(calc(a))
