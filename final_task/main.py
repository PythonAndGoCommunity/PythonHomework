import re


inp = '8*5-4+7*2'


regularExpression = r'(?:\d+(?:\.\d*)?|\.\d+)|[\+\-\*\/]'
parsedArray = re.findall(regularExpression, inp)

print(parsedArray)

priority = [
    ['+', '-'],
    ['*', '/'],
    ['(', ')', '^']
]

operation = {'+': lambda a, b: a+b,
             '-': lambda a, b: a-b,
             '*': lambda a, b: a*b,
             '/': lambda a, b: a/b
             }

maxPriority = len(priority)-1


class Token:
    def __init__(self, value, token_priority, array_index):
        self.value = value
        self.priority = token_priority
        self.array_index = array_index

    def __repr__(self):
        return "{}".format(self.value)


class Tree:
    def __init__(self, value, parent=None):
        self.rightNode = None
        self.leftNode = None
        self.token = value
        self.parent = parent

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


def build_tree(arr, parent=None):
    root = Tree(Token(None, maxPriority, None), parent)
    for token in arr:
        if root.token.priority >= token.priority:
            root.token = token

    if root.token.value is None:
        root.token = arr[0]

    border = arr.index(root.token)

    if root.token != arr[0]:
        root.leftNode = build_tree(arr[:border:], root)
        root.rightNode = build_tree(arr[border + 1::], root)
    return root


tree = build_tree(tokensArray)


result = 0

operands_array = []


def postOrder(node):
    if not node.leftNode and not node.rightNode:
        return node
    left = postOrder(node.leftNode)
    right = postOrder(node.rightNode)
    if left and right:
        result = operation[left.parent.token.value](int(left.token.value), int(right.token.value))
        left.parent.token.value = result
        return left.parent

print(postOrder(tree))


