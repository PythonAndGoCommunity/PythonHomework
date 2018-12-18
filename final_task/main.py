import re


inp = '8*5-4+7*2'


regExpression = r'(?:\d+(?:\.\d*)?|\.\d+)|[\+\-\*\/]'
result = re.findall(regExpression, inp)
print(result)

priority = [
    ['+', '-'],
    ['*', '/', '^'],
    ['(', ')']
]

tokens = []


class Token:
    def __init__(self, value, token_priority, index):
        self.value = value
        self.priority = token_priority
        self.index = index

    def __repr__(self):
        return "Token: {}, priority: {}".format(self.value, self.priority)


class Tree:
    def __init__(self, token):
        self.rightNode = None
        self.leftNode = None
        self.token = token

    def insert(self, value):
        pass

    def __repr__(self):
        return '{} (index = {})'.format(self.token.value, self.token.index)


for i, token in enumerate(result):
    for tokenPriority, operators in enumerate(priority):
        if token in operators:
            tokens.append(Token(token, tokenPriority, i))


root = Tree(Token(None, 3, None))

for token in tokens:
    if root.token.priority > token.priority:
        root.token = token

print(root)