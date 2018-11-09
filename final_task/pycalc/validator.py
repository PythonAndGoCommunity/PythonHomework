"""Tools for validating given expressions."""

import re


class Validator:
    """Validator checks given expression for possible errors."""

    def validate(self, expression):
        """Fully validates given expression for user error"""

        if len(expression) == 0:
            print("ERROR: cannot calculate empty expression.")
            exit(1)

        if expression.count('(') != expression.count(')'):
            print("ERROR: brackets are not balanced.")
            exit(1)

        pattern = r'[0-9]+\s+[0-9]+'
        if re.search(pattern, expression) is not None:
            print("ERROR: ambiguous spaces between numbers.")
            exit(1)

        pattern = r'[<>=*\/]\s+[<>=*\/]'
        if re.search(pattern, expression) is not None:
            print("ERROR: ambiguous spaces between signs.")
            exit(1)

    def check(self, sign, left, right):
        """Rapidly checks mathematical errors."""

        if left is None or right is None:
            print("ERROR: please, check your expression.")
            exit(1)

        if sign == '^' and left < 0 and isinstance(right, float):
            print("negative number cannot be raised to a fractional power.")
            exit(1)
