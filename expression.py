#!/usr/bin/python3


class BaseExpressionException(Exception):
    pass


class NoExpressionException(BaseExpressionException):
    pass


class BracketsAreNotBalanced(BaseExpressionException):
    pass


class DoubleOperationException(BaseExpressionException):
    pass


class Element:

    def __init__(self, expression):
        if not expression:
            raise NoExpressionException("The expression was not passed")

        self._expression = []

        bracket_level = 0
        item = []
        act = None

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
                    if i in ("/", "*",):
                        if act == i:
                            del self._expression[-1]
                            i = i * 2
                        act = i
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
        first_negative = False

        if self._expression[0] == "-":
            first_negative = True
            del self._expression[0]

        # Calculate high priority math operations
        for i in self._expression:
            if i in ("*", "/", "%", "//", "**",):
                if operation:
                    raise DoubleOperationException("'{so}' operation follows '{fo}'".format(
                        so=i,
                        fo=operation
                    ))
                operation = i
            elif operation:
                if isinstance(i, Element):
                    i = i.value()
                if operation == "*":
                    new_expression[-1] *= i
                elif operation == "/":
                    new_expression[-1] /= i
                elif operation == "%":
                    new_expression[-1] %= i
                elif operation == "//":
                    new_expression[-1] //= i
                elif operation == "**":
                    new_expression[-1] **= i
                operation = None
            else:
                if first_negative:
                    i = -i
                    first_negative = False
                new_expression.append(i)

        self._expression = new_expression

        # Calculate low priority math operations

        value = 0
        action = None

        for i in self._expression:
            if i in ("+", "-",):
                if action:
                    raise DoubleOperationException("'{so}' operation follows '{fo}'".format(
                        so=i,
                        fo=action
                    ))
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
    expr = Element("-2//3+7")

    print(str(expr))
    print(expr.value())
    # print(str(expr))
    # print(expr.value())
