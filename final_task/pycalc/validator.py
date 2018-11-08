"""Tools for validating given expressions."""

import re


class Validator:
    """Validator checks given expression for possible errors."""

    def validate(self, expression):
        """Fully validates given expression for user error"""

        if expression.count('(') != expression.count(')'):
            raise ValueError("brackets are not balanced")

        pattern = r'[0-9]+\s+[0-9]+'
        if re.search(pattern, expression) is not None:
            raise ValueError("ambiguous spaces between numbers")

        pattern = r'[<>=*\/]\s+[<>=*\/]'
        if re.search(pattern, expression) is not None:
            raise ValueError("ambiguous spaces between signs")

    def check(self, sign, left, right):
        """Rapidly checks mathematical errors."""

        if left is None or right is None:
            raise ValueError("please, check your expression")

        if sign == '^' and left < 0 and isinstance(right, float):
            error = "negative number cannot be raised to a fractional power"
            raise ValueError(error)
