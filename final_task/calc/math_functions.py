import math


functions_mapping = {
    'abs': math.fabs,
    'acos': math.acos,
    'acosh': math.acosh,
    'asin': math.asin,
    'asinh': math.asinh,
    'atan': math.atan,
    'atanh': math.atanh,
    'ceil': math.ceil,
    'cos': math.cos,
    'degrees': math.degrees,
    'exp': math.exp,
    'expm1': math.expm1,
    'fabs': math.fabs,
    'factorial': math.factorial,
    'log10': math.log10,
    'log2': math.log2,
    'radians': math.radians,
    'sin': math.sin,
    'round': round,
    'log': math.log,
    'pow': math.pow,
}


def decide_func(function, ready_args):
    for name, func in functions_mapping.items():
        if function == name:
            try:
                if len(ready_args) == 1:
                    return float(func(ready_args[0]))
                elif len(ready_args) == 2:
                    return float(func(ready_args[0], ready_args[1]))
                else:
                    print('ERROR: problem with arguments in function "' + function + '"!')
                    exit()
            except Exception:
                print('ERROR: problem with arguments in function "' + function + '"!')
                exit()
    print('ERROR: not find function "' + function + '"!')
    exit()
