"""Unittest for module exeptions."""

import unittest

from pycalc_src.exceptions import BaseCalculatorException
from pycalc_src.exceptions import CalculatorError


class TestStringMethods(unittest.TestCase):
    """Docstring."""

    def test_base_calculator_exeption__valid_expressions(self):
        """Docstring."""

        with self.assertRaises(BaseCalculatorException):
            raise CalculatorError(None, 0)


if __name__ == '__main__':
    unittest.main()
