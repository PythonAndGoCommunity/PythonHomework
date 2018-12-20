import re
import math

"""import argparse
parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
parser.add_argument("EXPRESSION", type=str,
                    help="expression string to evaluate")
args = parser.parse_args()
inp = args.EXPRESSION"""

inp = '1+cos(0)'

functions = {name: func for name, func in math.__dict__.items() if not name.startswith('__') and callable(func)}
functions.update({'abs': lambda a: abs(a), 'round': lambda a: round(a)})

constants = {name: const for name, const in math.__dict__.items() if not name.startswith('__') and not callable(const)}


operations = list(['(', ')',
                  {'<': lambda a, b: a < b,
                   '>': lambda a, b: a > b,
                   '<=': lambda a, b: a <= b,
                   '>=': lambda a, b: a >= b,
                   '!=': lambda a, b: a != b,
                   '==': lambda a, b: a == b}])
operations.append({'+': lambda a, b: a+b,
                   '-': lambda a, b: a-b})

operations.append({'*': lambda a, b: a*b,
                   '/': lambda a, b: a/b,
                   '//': lambda a, b: a//b,
                   '%': lambda a, b: a % b})

operations.append({'^': lambda a, b: a**b})
operations.append(functions)
func_reg = ''
for func in functions:
    func_reg += r'|(?:{})'.format(func)
const_reg = ''
for const in constants:
    const_reg += r'|(?:{})'.format(const)

regularExpression = r'(?:\d+(?:\.\d*)?|\.\d+)|' \
                    r'(?://)|(?:<=)|(?:!=)|(?:>=)|(?:==)|'\
                    r'[\+\-\*\/\%\^\(\)\<\>]'+func_reg+const_reg

parsedArray = re.findall(regularExpression, inp)


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
    for tokenPriority, operators in enumerate(operations):
        if token in operators:
            if token in functions:
                tokensArray.append(Token(token, 'function', tokenPriority))
            else:
                tokensArray.append(Token(token, 'operator', tokenPriority))
            break
    else:
        if token in constants:
            token = constants[token]
            tokensArray.append(Token(token, type(token)))
        elif '.' in token:
            token = float(token)
            tokensArray.append(Token(token, type(token)))
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
    if elem.type == 'operator' or elem.type == 'function':
        if stack.len == 0:
            stack.push(elem)
        elif (elem.priority > stack.last.priority or elem.priority == 0) and elem.priority != 1:
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
            if i.priority > 1:
                output.append(i)
            stack.pop()
print(output)
for token in output:
    if token.type == 'operator':
        result = operations[token.priority][token.value](stack.items[-2].value, stack.items[-1].value)
        new_token = Token(result, type(result))
        stack.pop(2)
        stack.push(new_token)
    elif token.type == 'function':
        result = operations[token.priority][token.value](stack.items[-1].value)
        new_token = Token(result, type(result))
        stack.pop()
        stack.push(new_token)

    else:
        stack.push(token)

print(stack.last)
