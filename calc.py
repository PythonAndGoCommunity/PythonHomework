binary_operations = {
    "+": 0,
    "-": 0,
    "*": 1,
    "/": 1,
    "//": 1,
    "%": 1,
    "^": 2,
}


def calc(expression):
    stack = []
    expression = to_postfix(expression)
    for i in expression:
        if i.isnumeric():
            stack.append(i)
        else:
            b = int(stack.pop())
            a = int(stack.pop())
            if i == '+':
                stack.append(a + b)
            if i == '-':
                stack.append(a - b)
            if i == '*':
                stack.append(a * b)
            if i == '/':
                stack.append(a / b)
            if i == '//':
                stack.append(a // b)
            if i == '%':
                stack.append(a % b)
            if i == '^':
                stack.append(a ** b)
    return stack.pop()


def to_postfix(expression):
    res = []
    stack = []
    for i in expression.split():
        if i.isnumeric():
            res.append(i)
        elif i == '(':
            stack.append(i)
        elif i == ')':
            while stack[-1] != '(':
                res.append(stack.pop())
            stack.pop()
        elif i in binary_operations:
            if stack and stack[-1] in binary_operations and binary_operations[stack[-1]] >= binary_operations[i]:
                while stack and binary_operations[stack[-1]] >= binary_operations[i]:
                    res.append(stack.pop())
                stack.append(i)
            else:
                stack.append(i)
    for i in reversed(stack):
        res.append(i)
    return res


a = "2 ^ 3 + 2"
print(calc(a))
