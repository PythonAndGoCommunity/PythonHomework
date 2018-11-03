import re
import math

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
                copysign=2, fabs=1, factorial=1, floor=1, fmod=2, frexp=1, ldexp=2, fsum=1, isfinite=1, isinf=1,
                isnan=1, modf=1, trunc=1, exp=1, expm1=1, log1p=1, log2=1, pow=2, degrees=1, radians=1, cosh=1, sinh=1,
                tanh=1, acosh=1, asinh=1, atanh=1, erf=1, erfc=1, gamma=1, lgamma=1, inv=0, gcd=2, isclose=5,
                isdexp=1,
                )


constants = {
    "pi",
    "e",
    "tau",
    "inf",
    "nan",
}


comparison_operators = {
    "<",
    "<=",
    "==",
    "!=",
    ">=",
    ">",
}


def correct_expression(expression):
    re_expr = re.findall('<=|==|!=|>=|log10|log2|log1p|expm1|atan2|\//|\d+\.\d+|\d+|\W|\w+',expression)
    i = 0
    if re_expr[0] == '-' and is_float(re_expr[1]):
        re_expr[1] *= -1
        re_expr.pop(0)
    _len = lambda x: len(x)
    for i in range(_len(re_expr)):
        if is_float(re_expr[i]) and re_expr[i + 1] == '(':
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
        elif re_expr[i] == '(' and re_expr[i+1] == '-' and is_float(re_expr[i+2]):
            re_expr[i+2] =re_expr[i+1] + re_expr[i+2]
            re_expr.pop(i+1)

        if i + 2 >= _len(re_expr):
            break
    return re_expr


def get_arguments(expression):
    ops = expression.pop(0)
    res = []
    arg = []
    point = 1
    while expression:
        if expression[0] == ',':
            res.append(arg.copy())
            arg.clear()
        elif expression[0] == ')':
            point -= 1
            if point == 0:
                expression.remove(expression[0])
                res.append(arg)
                return ops, res
            else:
                arg.append(expression[0])
        elif expression[0] in ops_list:
            point += 1
            arg.append(expression[0])
        else:
            arg.append(expression[0])
        expression.remove(expression[0])


def is_float(val):
    try:
        float(val)
        return True
    except ValueError:
        return False


def calc(expression):
    stack = []
    while expression:
        i = expression[0]
        if is_float(i):
            stack.append(float(i))
            expression.remove(i)
        elif i in comparison_operators:
            operator = expression.pop(0)
            a = stack.pop()
            b = calc(expression)
            if operator == '<':
                res = a < b
            elif operator == '<=':
                res = a <= b
            elif operator == '==':
                res = a == b
            elif operator == '!=':
                res = a != b
            elif operator == '>=':
                res = a >= b
            elif operator == '>':
                res = a>b
            stack.append(res)
        elif i in constants:
            if i == "pi":
                stack.append(math.pi)
            elif i == "e":
                stack.append(math.e)
            elif i == "tau":
                stack.append(math.tau)
            elif i == "inf":
                stack.append(math.inf)
            elif i == "nan":
                stack.append(math.nan)
            expression.remove(i)
        elif i in binary_operations:
            if len(stack)>1 and isinstance(stack[-1],(int,float)) and isinstance(stack[-2],(int,float)):
                b = stack.pop()
                a = stack.pop()
                if i == '+':
                    stack.append(a + b)
                elif i == '-':
                    stack.append(a - b)
                elif i == '*':
                    stack.append(a * b)
                elif i == '/':
                    stack.append(a / b)
                elif i == '//':
                    stack.append(a // b)
                elif i == '%':
                    stack.append(a % b)
                elif i == '^':
                    stack.append(a ** b)
            else:
                stack.append(i)
            expression.remove((i))
        if i in ops_list:
            arg = []
            ops, arg0 = get_arguments(expression)
            while arg0:
               arg.append(calc(arg0.pop()))
            if ops == 'pow':
                stack.append(pow(*arg))
            elif ops == 'abs':
                stack.append(abs(*arg))
    print(stack)
    return stack.pop()


def to_postfix(expression):
    res = []
    stack = []
    ops_bracket = []
    for i in correct_expression(expression):
        if is_float(i) or i in ops_list or i in constants:
            res.append(i)
        elif i in comparison_operators:
            while stack:
                res.append(stack.pop())
            res.append(i)
        elif i == '(':
            if res[-1] in ops_list:
                ops_bracket.append(i)
            stack.append(i)
        elif i == ')':
            while stack[-1] != '(':
                res.append(stack.pop())
            stack.pop()
            if ops_bracket:
                ops_bracket.pop()
                res.append(i)
        elif i in binary_operations:
            if stack and stack[-1] in binary_operations and binary_operations[stack[-1]] >= binary_operations[i]:
                while stack and stack[-1] in binary_operations and binary_operations[stack[-1]] >= binary_operations[i]:
                    res.append(stack.pop())
                stack.append(i)
            else:
                stack.append(i)
        elif i == ',':
            while stack[-1] != '(':
                res.append(stack.pop())
            res.append(i)

    for i in reversed(stack):
        res.append(i)
    return res

 #a = calc(to_postfix('abs(2)+3*2'))
print('res', calc(to_postfix('abs(-2)+3*2')))
print(calc(to_postfix('pow(abs(3),abs(56-53)+1)+3*(3-4)+pi')))
print(calc(to_postfix('pow(abs(2+1-1),abs(56-53)+1)+3*(3-4)')))
print(calc(to_postfix("2+3-5+6<=6")))


