import operator
import math

OPERATORS = {'+': operator.add,
             '-': operator.sub,
             '*': operator.mul,
             '/': operator.truediv,
             '^': operator.pow,
             '%': operator.mod}

FUNCTIONS = ['abs',
             'sin',
             'cos',
             'log10',
             'log']


def checkBrackets(expression):
    bracketsAmount = 0
    for symbol in expression:
        if bracketsAmount == -1:
            return False
        if symbol == '(':
            bracketsAmount += 1
        elif symbol == ')':
            bracketsAmount -= 1
    if bracketsAmount != 0:
        return False
    return True


def allowedNums():
    return '0123456789.'


def convertExpr(expr):
    iter = 0
    i = 0
    out = ''
    for symbol in expr:
        if symbol == '-' and iter == 0:
            out += symbol
        elif symbol in allowedNums():
            out += symbol
            iter += 1
        elif symbol in OPERATORS:
            out += ' %s ' % (symbol)
            iter += 1
        if symbol == ')' and len(expr) == i+1:
            out += ' )'
            iter = 0
        elif symbol == ')' and expr[i+1] in allowedNums():
            out += ' ) * '
            iter += 1
        elif symbol == ')':
            out += ' )'
            iter += 1
        if symbol == '(' and iter == 0:
            out += '( '
            iter = 0
        elif symbol == '(' and expr[i-1] in allowedNums():
            out += ' * ( '
            iter = 0
        elif symbol == '(' and expr[i-1] == ')':
            out += ' * ( '
            iter = 0
        elif symbol == '(':
            out += '( '
            iter = 0
        i += 1
    return out.strip()


def calc(expr):
    stack = [0]
    for token in expr.split(' '):
        if token in OPERATORS:
            op2, op1 = stack.pop(), stack.pop()
            stack.append(OPERATORS[token](op1, op2))
        elif token:
            stack.append(float(token))
    return stack.pop()


def RevPolNot(expr):
    operators = {'+': 1,
                 '-': 1,
                 '*': 2,
                 '/': 2,
                 '^': 3,
                 '%': 2}
    RevPN = []
    stack = ['']
    for token in expr.split(' '):
        if token in operators:
            op = stack.pop()
            if op == '' or op == '(':
                stack.append(op)
                stack.append(token)
            elif operators[token] <= operators[op]:
                stack.append(token)
                RevPN.append(op)
            elif operators[token] > operators[op]:
                stack.append(op)
                stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            op = stack.pop()
            while not op == '(':
                RevPN.append(op)
                op = stack.pop()
        else:
            RevPN.append(token)
    while stack:
        RevPN.append(stack.pop())
    return ' '.join(RevPN)


def main():
    """Entry point"""

    parser = argparse.ArgumentParser(add_help=True, description="Pure-python command-line calculator.")
    parser.add_argument("EXPRESSION", type=str, help="expression string to evaluate")
    args = parser.parse_args()
    try:
        print(calc(RevPolNot(convertExpr(args.EXPRESSION))))
    except Exception as err:
        print('ERROR:', err)
