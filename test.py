#!/usr/bin/python3


# def in_total(self):
Element = "4/2+10*5"
new_expression = []
for i in Element:
    while i != "*":
        new_expression.append(i)
        if i == "*":
            new_expression[-1] = new_expression[-1] * Element[ 1]
            print(Element[i+1])
            print((new_expression))


