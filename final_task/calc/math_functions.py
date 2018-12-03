from math import *


def decide_func(func, ready_args):
    if len(ready_args) == 0:
        print('ERROR: no necessary arguments ')
        exit()

    elif len(ready_args) > 2:
        print('ERROR: so many arguments')
        exit()

    elif func == 'abs':
        return abs(ready_args[0])

    elif func == 'acos':
        return acos(ready_args[0])

    elif func == 'acosh':
        return acosh(ready_args[0])

    elif func == 'asin':
        return asin(ready_args[0])

    elif func == 'asinh':
        return asinh(ready_args[0])

    elif func == 'atan':
        return atan(ready_args[0])

    elif func == 'atanh':
        return atanh(ready_args[0])

    elif func == 'ceil':
        return ceil(ready_args[0])

    elif func == 'cos':
        return cos(ready_args[0])

    elif func == 'degrees':
        return degrees(ready_args[0])

    elif func == 'erf':
        return erf(ready_args[0])

    elif func == 'exp':
        return exp(ready_args[0])

    elif func == 'expm1':
        return expm1(ready_args[0])

    elif func == 'fabs':
        return fabs(ready_args[0])

    elif func == 'factorial':
        return factorial(ready_args[0])

    elif func == 'floor':
        return floor(ready_args[0])

    elif func == 'frexp':
        return frexp(ready_args[0])

    elif func == 'gamma':
        return gamma(ready_args[0])

    elif func == 'lgamma':
        return lgamma(ready_args[0])

    elif func == 'log10':
        return log10(ready_args[0])

    elif func == 'log1p':
        return log1p(ready_args[0])

    elif func == 'log2':
        return log2(ready_args[0])

    elif func == 'radians':
        return radians(ready_args[0])

    elif func == 'sin':
        return sin(ready_args[0])

    elif func == 'sinh':
        return sinh(ready_args[0])

    elif func == 'sqrt':
        return sqrt(ready_args[0])

    elif func == 'tan':
        return tan(ready_args[0])

    elif func == 'tanh':
        return tanh(ready_args[0])

    elif func == 'trunc':
        return trunc(ready_args[0])

    elif func == 'round':
        if len(ready_args) == 1:
            ready_args.append(0)
        return round(ready_args[0], int(ready_args[1]))

    elif func == 'log':
        if len(ready_args) == 1:
            ready_args.append(e)
        return log(ready_args[0], ready_args[1])

    elif len(ready_args) < 2:
        print('ERROR: no necessary arguments or our function "' + s[i] + '"')
        exit()

    elif func == 'atan2':
        return atan2(ready_args[0], ready_args[1])

    elif func == 'fmod':
        return fmod(ready_args[0], ready_args[1])

    elif func == 'gcd':
        return gcd(ready_args[0], ready_args[1])

    elif func == 'hypot':
        return hypot(ready_args[0], ready_args[1])

    elif func == 'copysign':
        return copysign(ready_args[0], ready_args[1])

    elif func == 'pow':
        return pow(ready_args[0], ready_args[1])

    elif func == 'ldexp':
        return ldexp(ready_args[0], ready_args[1])

    else:
        print('ERROR: not find function "' + func + '"')
        exit()
