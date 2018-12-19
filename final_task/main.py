import re
import math

inp = '(7+4)*(2+3)+8'
inp = '5^7/(5*8)+10'

regularExpression = r'(?:\d+(?:\.\d*)?|\.\d+)|(?://)|[\+\-\*\/\%\^\(\)]'
parsedArray = re.findall(regularExpression, inp)

operation = {'+': lambda a, b: a+b,
             '-': lambda a, b: a-b,
             '*': lambda a, b: a*b,
             '/': lambda a, b: a/b,
             '//': lambda a, b: a//b,
             '%': lambda a, b: a % b,
             '^': lambda a, b: a**b
             }

priority = [
    ['('],
    [')'],
    ['<', '<=', '!=', '>=', '>'],
    ['+', '-'],
    ['/', '*'],
    ['^']
]


class Token:
    def __init__(self, value, type=None, token_priority=None, array_index=None):
        self.value = value
        self.priority = token_priority
        self.array_index = array_index
        self.type = type

    def __repr__(self):
        return "{}".format(self.value)


tokensArray = []
for token in parsedArray:
    for tokenPriority, operators in enumerate(priority):
        if token in operators:
            tokensArray.append(Token(token, 'operator', tokenPriority))
            break
    else:
        if '.' in token:
            token = float(token)
        else:
            token = int(token)
            tokensArray.append(Token(token, type(token)))


output = []
operators = []


class Stack:
    def __init__(self, arr=[]):
        self.items = arr
        self.len = 0
        self.last = None

    def push(self, token):
        self.items.append(token)
        self.len += 1
        self.last = token

    def pop(self, count=1):
        for i in range(count):
            if self.len > 0:
                self.items.pop()
                self.len -= 1
                if self.len > 0:
                    self.last = self.items[-1]
            else:
                break

    def __iter__(self):
        return iter(self.items[::-1])

    def __repr__(self):
        return repr(self.items)


stack = Stack()

for elem in tokensArray:
    if elem.type == 'operator':
        if stack.len == 0:
            stack.push(elem)
        elif elem.priority > stack.last.priority or elem.priority == 0:
            stack.push(elem)

        else:
            for el in stack:
                if elem.priority == 1:
                    for i in stack:
                        if i.priority != 0:
                            output.append(i)
                            stack.pop()
                        else:
                            stack.pop()
                            break

                elif elem.priority <= el.priority:
                    stack.pop()
                    stack.push(elem)
                    output.append(el)
    else:
        output.append(elem)
else:
    if stack.len > 0:
        for i in stack:
            output.append(i)
            stack.pop()

print(tokensArray)
print(output)

for token in output:
    if token.type == 'operator':
        result = operation[token.value](stack.items[-2].value, stack.items[-1].value)
        new_token = Token(result, type(result))
        stack.pop(2)
        stack.push(new_token)
    else:
        stack.push(token)

print(stack)
