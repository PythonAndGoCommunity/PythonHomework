#!/usr/bin/python3


class BaseExpressionException(Exception):
    pass


class NoExpressionException(BaseExpressionException):
    pass


class BracketsAreNotBalanced(BaseExpressionException):
    pass


class DoubleOperationException(BaseExpressionException):
    pass


class ExpressionFormatException(BaseExpressionException):
    pass


class Element:
    MATH_ACTIONS = ("+", "-", "*", "/", "%", "^",)

    def __init__(self, expression):
        if not expression:
            raise NoExpressionException("The expression was not passed")

        self._expression = []

        bracket_level = 0
        item = []
        act = None
        bracket_closed = False

        for i in expression:
            if bracket_closed:
                if i not in self.MATH_ACTIONS and i != ")":
                    raise ExpressionFormatException("After bracket closed 'math sign' or "
                                                    "another bracket close are expected")
                bracket_closed = False

            if i == "(":
                bracket_level += 1
                if bracket_level == 1:
                    continue

            elif i == ")":
                bracket_level -= 1
                bracket_closed = True
                if bracket_level < 0:
                    raise BracketsAreNotBalanced("Closed non-opened bracket.")
                if bracket_level == 0:
                    if item:
                        self._expression.append(Element("".join(item)))
                        item.clear()
                    continue
            if bracket_level > 0:
                item.append(i)
            else:
                if i in self.MATH_ACTIONS:
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
                    act = None
        if bracket_level != 0:
            raise BracketsAreNotBalanced()

        if item:
            self._expression.append(float("".join(item)))

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

        # Validate mathematical operations
        last_operation = None
        for i in self._expression:
            if last_operation and i in self.MATH_ACTIONS:
                raise DoubleOperationException("'{so}' operation follows '{fo}'".format(
                    so=last_operation,
                    fo=i
                ))
            if i in self.MATH_ACTIONS:
                last_operation = i

        # Calculate high priority math operations
        for i in self._expression:
            if isinstance(i, Element):
                i = i.value()
            if i in ("*", "/", "%", "//", "**",):
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
        operation = None

        for i in self._expression:
            if isinstance(i, Element):
                i = i.value()
            if i in ("+", "-",):
                operation = i
            elif operation:
                if operation == "+":
                    value += i
                elif operation == "-":
                    value -= i
                operation = None
            else:
                value = i

        return value
