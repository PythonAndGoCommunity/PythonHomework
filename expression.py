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

    def value(self):
        new_expression = []
        operation = None

        # Calculate high priority math operations
        for i in self._expression:
            if i in ("*", "/", "%", "//",):
                operation = i
            elif operation:
                if operation == "*":
                    new_expression[-1] *= i
                elif operation == "/":
                    new_expression[-1] /= i
                elif operation == "%":
                    new_expression[-1] %= i
                elif operation == "//":
                    new_expression[-1] //= i
                operation = None
            else:
                new_expression.append(i)

        self._expression = new_expression

        # Calculate low priority math operations

        value = 0
        action = None

        for i in self._expression:
            if i in ("+", "-",):
                action = i
            elif action:
                if action == "+":
                    value += i
                elif action == "-":
                    value -= i
                action = None
            else:
                value = i
        return value


if __name__ == '__main__':
    expr = Element("-9/2+5*2")

    print(str(expr))
    print(expr.value())
    print(str(expr))
    print(expr.value())
