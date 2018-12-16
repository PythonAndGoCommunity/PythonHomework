"""Preprocessing module."""

from pycalc_src.exceptions import PreprocessingError

from pycalc_src.operators import OPERATORS
from pycalc_src.operators import CONSTANTS


class Preprocessor:
    """Preprocessor object."""

    def __init__(self, expression):
        self.expression = expression
        self.__return_code = 1

    def preprocessing(self):
        """Prepare expression for calculate."""
        if not self.expression:
            raise PreprocessingError('expression is empty', self.__return_code)

        if not isinstance(self.expression, str):
            raise PreprocessingError('expression is not a string', self.__return_code)

        if self.expression.count('(') != self.expression.count(')'):
            raise PreprocessingError('brackets are not balanced', self.__return_code)

        self.expression = self.expression.lower()

        self.expression = self.expression.replace('**', '^')

        self._clean_repeatable_operators()

        return self.expression

    def _clean_repeatable_operators(self):
        """Delete from string repeatable operators."""
        repeatable_operators = {'+-': '-', '--': '+', '++': '+', '-+': '-'}

        while True:
            old_exp = self.expression
            for old, new in repeatable_operators.items():
                self.expression = self.expression.replace(old, new)
            if old_exp == self.expression:
                break
