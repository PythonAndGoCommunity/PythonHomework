class Operator:
    def __init__(self, name, priority, associativity, is_binary,  func):
        self.priority = priority
        self.associativity = associativity
        self.func = func
        self.name = name
        self.is_binary = is_binary


class Function:
    def __init__(self, name, priority, associativity, is_binary,  func):
        self.priority = priority
        self.associativity = associativity
        self.func = func
        self.name = name
        self.is_binary = is_binary


class Constant:
    def __init__(self, name, priority, associativity, is_binary,  func):
        self.priority = priority
        self.associativity = associativity
        self.func = func
        self.name = name
        self.is_binary = is_binary


operators_dict = {
    '>=': Operator('>=', 0, 1, True, lambda x, y: x >= y),
    '<=': Operator('<=', 0, 1, True, lambda x, y: x <= y),
    '==': Operator('==', 0, 1, True, lambda x, y: x == y),
    '!=': Operator('!=', 0, 1, True, lambda x, y: x != y),
    '>': Operator('>', 0, 1, True, lambda x, y: x > y),
    '<': Operator('<', 0, 1, True, lambda x, y: x >= y),
    ',': Operator(',', 1, 1, True, lambda x, y: [x, y]),
    '+': Operator('+', 2, 1, True, lambda x, y: x+y),
    '-': Operator('-', 2, 1,  True, lambda x, y: x-y),
    ')': Operator(')', -1, 1, False, None),
    '(': Operator('(', -1, 1, False, None),
    '*': Operator('*', 3, 1, True, lambda x, y: x*y),
    '/': Operator('/', 3, 1, True, lambda x, y: x/y),
    '%': Operator('%', 3, 1, True, lambda x, y: x % y),
    '//': Operator('//', 3, 1, True, lambda x, y: x // y),
    'unary_minus': Operator('unary_minus', 5, 1, False, lambda x: -x),
    'unary_plus': Operator('unary_plus', 5, 1, False, lambda x: x),
    '^': Operator('^', 4, 2, True, lambda x, y: x**y),
}
