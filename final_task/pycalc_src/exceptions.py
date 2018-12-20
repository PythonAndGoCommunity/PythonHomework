"""Exceptions module."""


class BaseCalculatorException(Exception):
    """Base calculator exception."""

    def __init__(self, message=None, return_code=1):
        """"Init."""
        if message is None:
            message = 'an error occured while working pycalc'
        self.message = 'ERROR: {}'.format(message)

        if return_code == 1:
            print(self.message)
            exit(return_code)


class CalculatorError(BaseCalculatorException):
    """Exception for calculator."""

    def __init__(self, message=None, return_code=1):
        """"Init."""
        super().__init__(message, return_code)


class PreprocessingError(BaseCalculatorException):
    """Exception for preprocessing."""

    def __init__(self, message=None, return_code=1):
        """"Init."""
        super().__init__(message, return_code)
