import re


inp = '8*5-4+7*2'


regularExpression = r'(?:\d+(?:\.\d*)?|\.\d+)|[\+\-\*\/]'
parsedArray = re.findall(regularExpression, inp)

print(parsedArray)

priority = [
    ['+', '-'],
    ['*', '/', '^'],
    ['(', ')']
]
maxPriority = len(priority)-1


class Token:
    def __init__(self, value, token_priority, array_index):
        self.value = value
        self.priority = token_priority
        self.array_index = array_index

    def __repr__(self):
        return "{}".format(self.value)


class Tree:
    def __init__(self, value):
        self.rightNode = None
        self.leftNode = None
        self.token = value

    def __repr__(self):
        return "{}".format(self.token)


tokensArray = []
for i, token in enumerate(parsedArray):
    for tokenPriority, operators in enumerate(priority):
        if token in operators:
            tokensArray.append(Token(token, tokenPriority, i))
            break
    else:
        tokensArray.append(Token(token, maxPriority, i))


def build_tree(arr):
    root = Tree(Token(None, maxPriority, None))
    for token in arr:
        if root.token.priority > token.priority:
            root.token = token
    if root.token.value is None:
        root.token = arr[0]

    border = arr.index(root.token)

    if root.token != arr[0]:
        root.leftNode = build_tree(arr[:border:])
        root.rightNode = build_tree(arr[border + 1::])
    return root


tree = build_tree(tokensArray)
