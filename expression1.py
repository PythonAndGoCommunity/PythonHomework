#!/usr/bin/python3


class BaseExpressionException(Exception):
    pass


class NoExpressionException(BaseExpressionException):
    pass


class BracketsAreNotBalanced(BaseExpressionException):
    pass


class Element:

    def __init__(self, expression):
        if not expression:
            raise NoExpressionException("The expression was not passed")

        self._expression = []

        bracket_level = 0
        item = []

        for i in expression:
            if i == "(":
                bracket_level += 1
                if bracket_level == 1:
                    continue

            elif i == ")":
                bracket_level -= 1
                if bracket_level == 0:
                    if item:
                        self._expression.append(Element("".join(item)))
                        item.clear()
                    continue

            if bracket_level > 0:
                item.append(i)
            else:
                if i in ["+", "-", "*", "/", "%", "^"]:
                    if item:
                        self._expression.append(float("".join(item)))
                        item.clear()
                    self._expression.append(i)

                else:
                    item.append(i)

        if item:
            self._expression.append(float("".join(item)))

        if bracket_level != 0:
            raise BracketsAreNotBalanced()

    def __str__(self):
        result = []
        for i in self._expression:
            result.append(str(i))
        return "{cls_name}{{{data}}}".format(
            cls_name=self.__class__.__name__,
            data=", ".join(result)
        )

    def in_total(self):
        new_expression = []
        for i in range(len(self._expression)):

                new_expression.append(i)
                if self._expression[i] == "*":
                    new_expression[-1] = self._expression[i-1]*self._expression[i+1]
                        i=i+1
                if i == "/":
                    new_expression[-1] = new_expression[-1]/self._expression[i+1]




        return self._in_total


if __name__ == '__main__':
    expr = Element("4*2+10/5")

    print(str(expr))
    print(expr.in_total())
    # print(y)