"""Exceptions module."""
import sys


class BaseCalculatorException(Exception):
    """Base calculator exception."""

    def __init__(self, message=None):
        """"Init."""
        if message is None:
            message = 'an error occured while working pycalc'
        self.message = 'ERROR: {}'.format(message)

        print(self.message)

        exit(1)


class CalculatorError(BaseCalculatorException):
    """Exception for calculator."""

    def __init__(self, message=None):
        """"Init."""
        super().__init__(message)


class PreprocessingError(BaseCalculatorException):
    """Exception for preprocessing."""

    def __init__(self, message=None):
        """"Init."""
        super().__init__(message)
