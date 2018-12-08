"""
    Validator checks for possible error
    before and during the calculation.
"""

import re


class Validator:
    def validate(self, expression):
        """Fully validates given expression for user error"""

        if len(expression) == 0:
            self.assert_error("cannot calculate empty expression.")

        if expression.count('(') != expression.count(')'):
            self.assert_error("brackets are not balanced.")

        pattern = r'[0-9\.]+\s+[0-9\.]+'
        if re.search(pattern, expression) is not None:
            self.assert_error("ambiguous spaces between numbers.")

        pattern = r'[<>=*\/]\s+[<>=*\/]'
        if re.search(pattern, expression) is not None:
            self.assert_error("ambiguous spaces between signs.")

    def check(self, sign, left, right):
        """Rapidly checks mathematical errors."""

        if left is None or right is None:
            self.assert_error("please, check your expression.")

        if sign in ('/', '//', '%') and right == 0:
            self.assert_error("got a zero division error.")

        if sign == '^' and left < 0 and isinstance(right, float):
            self.assert_error(
                "negative number cannot be raised to fractional power."
            )

    @staticmethod
    def assert_error(error_text, exitcode=1):
        print("ERROR: " + error_text)
        exit(exitcode)
