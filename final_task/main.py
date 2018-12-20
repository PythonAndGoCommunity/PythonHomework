import re
import math
import error_list

"""import argparse
parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
parser.add_argument("EXPRESSION", type=str,
                    help="expression string to evaluate")
args = parser.parse_args()
inp = args.EXPRESSION"""


inp = 'sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)'

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

operations.append({'$': lambda a: -a})

operations.append({'*': lambda a, b: a*b,
                   '/': lambda a, b: a/b,
                   '//': lambda a, b: a//b,
                   '%': lambda a, b: a % b})

operations.append({'^': lambda a, b: a**b})
operations.append(functions)

func_reg = ''
temp_arr = []
for func in functions:
    temp_arr.append(func)
for func in reversed(temp_arr):
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
for index, token in enumerate(parsedArray):
    for tokenPriority, operators in enumerate(operations):
        if token in operators:
            if token in functions:
                tokensArray.append(Token(token, 'function', tokenPriority))
            else:
                if tokenPriority == 3:
                    if index == 0 or ((tokensArray[index-1].type == 'operator' or tokensArray[index-1].type == 'function') and tokensArray[index-1].priority != 1):
                        if token == '-':
                            tokensArray.append((Token('$', 'function', 4)))
                        break
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

if error_list.is_brackets_balanced(tokensArray) != 0:
    raise RuntimeError('ERROR: brackets are not balanced.')

if error_list.is_operations_missed(tokensArray):
    raise RuntimeError('ERROR: missing operations')

if not error_list.is_operations_ordered(tokensArray, operations):
    raise RuntimeError('ERROR: invalid operations order or missing operands')


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
                    self.last = None
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
            if elem.priority == 1:
                for i in stack:
                    if i.priority != 0:
                        output.append(i)
                        stack.pop()
                    else:
                        stack.pop()
                        break

            else:
                while stack.len > 0 and elem.priority <= stack.last.priority:
                    if len(output) == 0 and elem.value == '$':
                        break
                    output.append(stack.last)
                    stack.pop()
                stack.push(elem)
    else:
        output.append(elem)
else:
    if stack.len > 0:
        for i in stack:
            if i.priority > 1:
                output.append(i)
            stack.pop()

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
