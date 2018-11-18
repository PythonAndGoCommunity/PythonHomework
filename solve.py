#!/usr/bin/env python3

from libs.element import Element

if __name__ == '__main__':
    expression = Element(expression="(-2**4)-5*2*3")
    print(str(expression))
    print(expression.value())
