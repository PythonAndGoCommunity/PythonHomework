import io
import math
import tokenize

COMPARATORS = {
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '==': lambda x, y: x == y,
    '<=': lambda x, y: x <= y,
    '>=': lambda x, y: x >= y,
    '!=': lambda x, y: x != y}

PRIORITY = {'^': 3, '*': 2, '/': 2, '+': 1,
            '-': 1, '%': 1, '//': 1, '(': 0, ')': 0}

BINARY_OPERATORS = {
    '^': lambda x, y: x ** y,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '/': lambda x, y: x / y,
    '*': lambda x, y: x * y,
    '%': lambda x, y: x % y,
    '//': lambda x, y: x // y}

UNARY_OPERATORS = {'--': lambda x: - x,
                   '++': lambda x: x}

FUNCS = {k: v for k, v in math.__dict__.items()
         if not k.startswith('__') and callable(v)}

FUNCS.update({'abs': lambda x: abs(x),
              'round': lambda x: round(x)})

PREFIX = list(UNARY_OPERATORS.keys()) + list(FUNCS.keys())

CONSTANTS = {k: v for k, v in math.__dict__.items()
             if not k.startswith('__')and not callable(v)}


def isnumber(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


class Calculator:
    """
    Class for calculate a math expression

    Keywords Arguments:
        - expression -- A math expression to calculate or to compare
    """

    def __init__(self, expression):
        self.expression = expression
        self.right = []
        self.left = []
        self.comparator = None

    def calc(self):
        """Calculate an expression and return the result"""
        self.__split()
        if self.comparator:
            return COMPARATORS[self.comparator](self.__calc(self.__expression_to_rpn(self.__format_expression(
                self.left))), self.__calc(self.__expression_to_rpn(self.__format_expression(self.right))))
        return self.__calc(
            self.__expression_to_rpn(
                self.__format_expression(
                    self.expression)))

    def __calc(self, rpn):
        res = []
        for r in rpn:
            try:
                if r in FUNCS:
                    args = []
                    for _ in range(int(res.pop())):
                        args.append(res.pop())
                    args.reverse()
                    res.append(FUNCS[r](*args))
                elif r in UNARY_OPERATORS:
                    res.append(UNARY_OPERATORS[r](res.pop()))
                elif r in BINARY_OPERATORS:
                    x = res.pop()
                    y = res.pop()
                    res.append(BINARY_OPERATORS[r](y, x))
                else:
                    res.append(float(r))
            except (OverflowError):
                raise Exception('ERROR: Overflow')
            except (IndexError, ValueError):
                raise Exception(
                    "ERROR: expression is incorrect in '{}'".format(r))
            except (ZeroDivisionError):
                raise Exception("ERROR: zero division")
        if len(res) > 1:
            raise Exception(
                "ERROR: func or operator doesn\'t confrim the requirements")
        return res[0]

    def __expression_to_rpn(self, expression):
        rpn = []
        stack = []
        args = []
        open_bracket = False
        for e in expression:
            if isnumber(e):
                open_bracket = False
                rpn.append(e)
            elif e in PREFIX or e == '(':
                open_bracket = True
                stack.append(e)
                args.append(1) if e in FUNCS else None
            elif e == ',':
                open_bracket = False
                s = stack[-1]
                args[-1] += 1
                while s != '(':
                    s = stack.pop()
                    rpn.append(s)
                    s = stack[-1]
            elif e == ')':
                if open_bracket:
                    args[-1] = 0
                    open_bracket = False
                s = stack.pop()
                while s != '(':
                    rpn.append(s)
                    s = stack.pop()
                if args and len(args) == len(
                        list(filter(lambda x: x in FUNCS, stack))):
                    rpn.append(args.pop())
            elif e in BINARY_OPERATORS:
                open_bracket = False
                if stack:
                    s = stack[-1]
                    while (
                            s in PREFIX or PRIORITY[s] >= PRIORITY[e]) and e != '^':
                        s = stack.pop()
                        rpn.append(s)
                        if not stack:
                            break
                        s = stack[-1]
                stack.append(e)
            else:
                raise Exception('ERROR: unknown operator "{}"'.format(e))
        while stack:
            rpn.append(stack.pop())
        return rpn

    def __format_expression(self, expression):
        places_to_indent_mult = []
        expression = [str(CONSTANTS[e])
                      if e in CONSTANTS else e for e in expression]
        expression = ['^' if e == '**' else e for e in expression]
        # .1 to 0.1 conversion
        expression = ['0{}'.format(e) if e.replace(
            '.', '').isdigit() and e[0] == '.' else e for e in expression]
        # take adjacent elements to find places to insert implicit mult
        for i, (cur, next) in enumerate(zip(expression, expression[1:])):
            if (
                cur == ')' and next == '(') or (
                cur == ')' and isnumber(next)) or (
                isnumber(cur) and next == '(') or (
                isnumber(cur) and next in PREFIX) or (
                    cur in PREFIX and isnumber(next)) or (
                        cur == ')' and next in PREFIX):
                places_to_indent_mult.append(i + 1)
        # insert implicit mult
        for i, p in enumerate(places_to_indent_mult):
            expression.insert(i + p, '*')
        for s in ['-', '+']:
            try:
                if expression[0] == s and (
                    isnumber(
                        expression[1]) or expression[1] in PREFIX or expression[1] in [
                        '-',
                        '+']):
                    expression[0] = '{}{}'.format(s, s)
            except (IndexError):
                raise Exception('ERROR: where your expression?')
        # insert unary + or -
        for i, (cur, next) in enumerate(zip(expression, expression[1:])):
            if ((cur == '--' or cur == '++' or cur in BINARY_OPERATORS) and next == '-') or \
                    (cur == '(' and next == '-'):
                expression[i + 1] = '--'
            if ((cur == '--' or cur == '++' or cur in BINARY_OPERATORS) and next == '+') or \
                    (cur == '(' and next == '+'):
                expression[i + 1] = '++'
        return expression

    def __split(self):
        try:
            self.expression = [t[1] for t in tokenize.generate_tokens(
                io.StringIO(self.expression).readline) if t[1]]
        except(tokenize.TokenError):
            raise Exception('ERROR: brackets are not balanced')

        if any([c in COMPARATORS for c in self.expression]):
            if len(
                list(
                    filter(
                        lambda x: x in COMPARATORS,
                        self.expression))) > 1:
                raise Exception('ERROR: two or more comparasion operators')
            i = self.expression.index(
                [c for c in self.expression if c in COMPARATORS][0])
            self.comparator = self.expression[i]
            self.left = self.expression[0:i]
            self.right = self.expression[i + 1:]
