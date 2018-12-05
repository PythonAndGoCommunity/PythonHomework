#!/usr/bin/python3

import math

from inspect import getmembers


class BaseExpressionException(Exception):
    """ Common base class for all exceptions """
    pass


class NoExpressionException(BaseExpressionException):
    """ Class exception for no expression. """
    pass


class BracketsAreNotBalanced(BaseExpressionException):
    """ Class exception for expression when brackets are not balanced. """
    pass


class DoubleOperationException(BaseExpressionException):
    """ Class exception for expression with double operation. """
    pass


class ExpressionFormatException(BaseExpressionException):
    """ Class exception for expression with not correct format. """
    pass


class UnsupportedMathematicalOperationException(ExpressionFormatException):
    """ Class exception for expression with not correct mathematical operations. """
    pass


class UnsupportedMathematicalFunctionException(ExpressionFormatException):
    """ Class exception for expression with unsupported mathematical function. """
    pass


class Element:
    """
    Base class for parsing and calculation the mathematical expression. Check the expression for the number of brackets.
    Perform the transformation of the expression, depending on the number of brackets. If brackets an odd number raise
    exception. Parse the expression into the components, separate mathematical operations and numbers. And create new
    expression. Validate format expression. Validate first negative numbers in expression. Validate mathematical
    operations and calculate nested expressions. Calculate high priority math operations.Calculate low priority math
    operations.
    """

    MATH_ACTIONS = ("+", "-", "*", "/", "%", "^",)
    COMPARISON_OPERATIONS = (">", "<", "=", "!",)

    def __init__(self, expression, func=None):
        """
        Class constructor
        :param expression: mathematical expression as string
        """
        # Validate on expression and raise exception if not true
        expression = expression.replace(" ", "")
        if not expression:
            raise NoExpressionException("The expression was not passed")

        # TODO: comment
        self._mathematical_functions = {
            name: val for name, val in getmembers(math) if type(val).__name__ == "builtin_function_or_method"
        }
        self._mathematical_functions["abs"] = abs
        self._mathematical_functions["round"] = round

        self._mathematical_constants = {
            name: val for name, val in getmembers(math) if type(val).__name__ == "float"
        }

        self._func = None
        if func:
            if func not in self._mathematical_functions:
                raise UnsupportedMathematicalFunctionException("We do not support '{}' function".format(self._func))
            self._func = self._mathematical_functions.get(func)

        self._expression = []

        bracket_level = 0
        item = []
        last_mathematical_action = None
        bracket_closed = False
        bracket_content = []
        self._comparison_operation = False
        self._multivalue = False

        # Validate expression on comparison operation and raise exception if it has not valid format
        previous_is_comparison = False
        for i, v in enumerate(expression):
            if v in self.COMPARISON_OPERATIONS:
                self._comparison_operation = True
                if item:
                    self._expression.append(Element("".join(item)))
                    item.clear()

                if previous_is_comparison:
                    self._expression[-1] += v
                else:
                    self._expression.append(v)

                previous_is_comparison = True
            else:
                previous_is_comparison = False
                item.append(v)

        if self._comparison_operation:
            if item:
                self._expression.append(Element("".join(item)))
                return
            else:
                raise ExpressionFormatException("After comparison operation expression or number are expected")

        # Look for multivalue expression
        if "(" not in expression and ")" not in expression and "," in expression:
            if not self._func:
                raise ExpressionFormatException("Commas allowed only in function calls.")
            parts = expression.split(",")
            self._expression = [Element(i) for i in parts]
            self._multivalue = True
            return

        # Validate format expression and raise exception if it is not valid
        item = []
        for i in expression:
            if bracket_closed:
                if i not in self.MATH_ACTIONS and i != ")":
                    raise ExpressionFormatException("After bracket closed 'math sign' or "
                                                    "another bracket close are expected")
                bracket_closed = False

            # Validate  and count brackets
            if i == "(":
                bracket_level += 1
                if bracket_level == 1:
                    continue

            # Validate and sorted data in brackets
            elif i == ")":
                bracket_level -= 1
                bracket_closed = True
                if bracket_level < 0:
                    raise BracketsAreNotBalanced("Closed non-opened bracket.")
                if bracket_level == 0:
                    if bracket_content:
                        if item:
                            self._expression.append(Element(expression="".join(bracket_content), func="".join(item)))
                            item.clear()
                        else:
                            self._expression.append(Element("".join(bracket_content)))
                        bracket_content.clear()
                    else:
                        raise ExpressionFormatException("Empty brackets.")
                    continue

            if bracket_level > 0:
                bracket_content.append(i)
            else:
                if i in self.MATH_ACTIONS:
                    if item:
                        item = "".join(item)
                        if item in self._mathematical_constants:
                            item = self._mathematical_constants[item]
                        self._expression.append(float(item))
                        item = []

                    # Handle double mathematical operation
                    if last_mathematical_action == i:
                        self._expression[-1] += i
                    else:
                        self._expression.append(i)
                    last_mathematical_action = i

                else:
                    item.append(i)
                    last_mathematical_action = None
        if bracket_level != 0:
            raise BracketsAreNotBalanced()

        # Add item after parsing
        if item:
            item = "".join(item)
            if item in self._mathematical_constants:
                item = self._mathematical_constants[item]
            try:
                self._expression.append(float(item))
            except ValueError:
                raise ExpressionFormatException("Could not convert string to float: '{}'".format(item))

    def __str__(self):
        """
        String representation of the class
        :return: string representation of the class
        """
        result = []
        for i in self._expression:
            result.append(str(i))
        return "{cls_name}{{{data}}}".format(
            cls_name=self.__class__.__name__,
            data=", ".join(result)
        )

    def _calculate_boolean_expression(self):
        boolean_value = True
        for i, v in enumerate(self._expression):
            if isinstance(v, str):
                if v == ">=":
                    if not self._expression[i - 1] >= self._expression[i + 1]:
                        boolean_value = False
                elif v == "<=":
                    if not self._expression[i - 1] <= self._expression[i + 1]:
                        boolean_value = False
                elif v == "==":
                    if not self._expression[i - 1] == self._expression[i + 1]:
                        boolean_value = False
                elif v == "<":
                    if not self._expression[i - 1] < self._expression[i + 1]:
                        boolean_value = False
                elif v == ">":
                    if not self._expression[i - 1] > self._expression[i + 1]:
                        boolean_value = False
                elif v in ("!=", "<>",):
                    if not self._expression[i - 1] != self._expression[i + 1]:
                        boolean_value = False
                else:
                    raise UnsupportedMathematicalOperationException("We do not support '{}' operation".format(v))

            if not boolean_value:
                return boolean_value
        return boolean_value

    def _calculate_mathematical_expression(self):
        operation = None
        first_negative = False

        # Validate first negative numbers in expression
        if self._expression[0] == "-":
            first_negative = True
            del self._expression[0]

        # Calculate power mathematical operation
        self._expression.reverse()
        while True:
            try:
                index = self._expression.index("^")
                self._expression.pop(index)
                power = self._expression.pop(index - 1)
                self._expression[index - 1] **= power
            except ValueError:
                break
        self._expression.reverse()

        # Calculate high priority mathematical operations
        new_expression = []
        for i in self._expression:
            if i in ("*", "/", "%", "//", "**"):
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
                    raise UnsupportedMathematicalOperationException("We do not support '{}' operation".format(i))
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
            if isinstance(i, str):
                if i in ("+", "-",):
                    operation = i
                else:
                    raise UnsupportedMathematicalOperationException("We do not support '{}' operation".format(i))
            elif operation:
                if operation == "+":
                    value += i
                elif operation == "-":
                    value -= i
                operation = None
            else:
                value = i

        # Validate on mathematical function
        if self._func:
            value = self._func(value)

        return value

    def value(self):
        """
        Method for expression calculation
        :return: calculate value
        """

        # Validate mathematical operations and calculate nested expressions
        last_operation = None
        for i, v in enumerate(self._expression):
            if isinstance(v, Element):
                self._expression[i] = v.value()
            if isinstance(v, str):
                if v not in ("<=", ">=", "==", "!=", "<>", "**", "//"):
                    if len(v) > 1:
                        if len(v) % 2 == 0:
                            self._expression[i] = "+"
                        else:
                            self._expression[i] = "-"

            if last_operation and v in ("+", "-",):
                if last_operation == "+" and v == "-":
                    self._expression[i] = "-"
                    del self._expression[i - 1]
                elif last_operation == "-" and v == "+":
                    self._expression[i] = "-"
                    del self._expression[i]
            elif last_operation and v in self.MATH_ACTIONS:
                raise DoubleOperationException("'{so}' operation follows '{fo}'".format(
                    so=last_operation,
                    fo=v
                ))

            if v in self.MATH_ACTIONS:
                last_operation = v
            else:
                last_operation = None

        # Evaluate comparison expression
        if self._comparison_operation:
            return self._calculate_boolean_expression()

        # Evaluate multi-value expression
        if self._multivalue:
            try:
                return self._func(*self._expression)
            except TypeError:
                raise ExpressionFormatException("Expected 2 arguments, got 3: '{}'".format(self._func))

        try:
            return self._calculate_mathematical_expression()
        except TypeError:
            raise UnsupportedMathematicalOperationException("We do not support '{}' operation".format(i))
