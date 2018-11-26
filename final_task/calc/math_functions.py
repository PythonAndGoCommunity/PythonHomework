from math import *


def decide_func(s, i, ready_args):
    """determinate functions"""
    if len(ready_args) == 0:
        print('ERROR: no necessary arguments ')
        exit(AttributeError)
    elif len(ready_args) > 2:
        print('ERROR: so many arguments')
        exit(AttributeError)
    elif s[i] == 'abs':
        s[i] = abs(ready_args[0])
    elif s[i] == 'acos':
        s[i] = acos(ready_args[0])
    elif s[i] == 'acosh':
        s[i] = acosh(ready_args[0])
    elif s[i] == 'asin':
        s[i] = asin(ready_args[0])
    elif s[i] == 'asinh':
        s[i] = asinh(ready_args[0])
    elif s[i] == 'atan':
        s[i] = atan(ready_args[0])
    elif s[i] == 'atanh':
        s[i] = atanh(ready_args[0])
    elif s[i] == 'ceil':
        s[i] = ceil(ready_args[0])
    elif s[i] == 'cos':
        s[i] = cos(ready_args[0])
    elif s[i] == 'degrees':
        s[i] = degrees(ready_args[0])
    elif s[i] == 'erf':
        s[i] = erf(ready_args[0])
    elif s[i] == 'exp':
        s[i] = exp(ready_args[0])
    elif s[i] == 'expm1':
        s[i] = expm1(ready_args[0])
    elif s[i] == 'fabs':
        s[i] = fabs(ready_args[0])
    elif s[i] == 'factorial':
        s[i] = factorial(ready_args[0])
    elif s[i] == 'floor':
        s[i] = floor(ready_args[0])
    elif s[i] == 'frexp':
        s[i] = frexp(ready_args[0])
    elif s[i] == 'gamma':
        s[i] = gamma(ready_args[0])
    elif s[i] == 'lgamma':
        s[i] = lgamma(ready_args[0])
    elif s[i] == 'log10':
        s[i] = log10(ready_args[0])
    elif s[i] == 'log1p':
        s[i] = log1p(ready_args[0])
    elif s[i] == 'log2':
        s[i] = log2(ready_args[0])
    elif s[i] == 'radians':
        s[i] = radians(ready_args[0])
    elif s[i] == 'sin':
        s[i] = sin(ready_args[0])
    elif s[i] == 'sinh':
        s[i] = sinh(ready_args[0])
    elif s[i] == 'sqrt':
        s[i] = sqrt(ready_args[0])
    elif s[i] == 'tan':
        s[i] = tan(ready_args[0])
    elif s[i] == 'tanh':
        s[i] = tanh(ready_args[0])
    elif s[i] == 'trunc':
        s[i] = trunc(ready_args[0])
    elif s[i] == 'round':
        if len(ready_args) == 1:
            ready_args.append(0)
        s[i] = round(ready_args[0], int(ready_args[1]))
    elif s[i] == 'log':
        if len(ready_args) == 1:
            ready_args.append(e)
        s[i] = log(ready_args[0], ready_args[1])
    elif len(ready_args) < 2:
        print('ERROR: no necessary arguments or our function "' + s[i] + '"')
        exit(AttributeError)
    elif s[i] == 'atan2':
        s[i] = atan2(ready_args[0], ready_args[1])
    elif s[i] == 'fmod':
        s[i] = fmod(ready_args[0], ready_args[1])
    elif s[i] == 'gcd':
        s[i] = gcd(ready_args[0], ready_args[1])
    elif s[i] == 'hypot':
        s[i] = hypot(ready_args[0], ready_args[1])
    elif s[i] == 'copysign':
        s[i] = copysign(ready_args[0], ready_args[1])
    elif s[i] == 'pow':
        s[i] = pow(ready_args[0], ready_args[1])
    elif s[i] == 'ldexp':
        s[i] = ldexp(ready_args[0], ready_args[1])
    else:
        print('ERROR: no function "' + s[i] + '"')
        exit(AttributeError)
