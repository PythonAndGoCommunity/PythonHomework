"""Calculator module."""

from pycalc_src.exceptions import CalculatorError

from pycalc_src.operators import OPERATORS
from pycalc_src.operators import CONSTANTS
from pycalc_src.operators import UNARY_OPERATORS
from pycalc_src.operators import COMPARISON_SYMBOLS

from pycalc_src.preprocessor import Preprocessor


class Calculator:
    """Calculator object."""

    def __init__(self, expression):
        self.expression = expression
        self.number = ''
        self.operator = ''
        self.unary_operator = ''
        self.rpn = []
        self.stack = []
        self.__return_code = 1

    def _process_digit(self, index, symbol):
        """Process digit from expression."""
        if self.expression[index - 1] == ' ' and self.number:
            raise CalculatorError('invalid syntax', self.__return_code)
        self.number += symbol

    def _process_number_and_constant(self):
        """Process number and constant."""
        if self.unary_operator:
            self.unary_operator = self._replace_unary_operator(self.unary_operator)

        if self.number:
            self.rpn.append(self._convert_to_number('{}{}'.format(self.unary_operator,
                                                                  self.number)))
            self.number = ''

        if self.operator in CONSTANTS:

            if self.rpn and self.rpn[-1] in CONSTANTS.values():
                self.stack.append('*')

            if self.unary_operator == '-':
                self.rpn.append(0 - CONSTANTS[self.operator])
            else:
                self.rpn.append(CONSTANTS[self.operator])
            self.operator = ''

        self.unary_operator = ''

    def _process_operator(self):
        """Process operator."""
        if self.unary_operator:
            self.stack.append(self.unary_operator)

        if self.operator:
            if self.operator not in OPERATORS:
                raise CalculatorError('operator not supported', self.__return_code)
            self.stack.append(self.operator)

        self.unary_operator = ''
        self.operator = ''

    def _process_stack(self, symbol):
        """Process stack."""
        while self.stack:
            if self.stack[-1] == symbol == '^':
                break

            if OPERATORS[symbol].priority <= OPERATORS[self.stack[-1]].priority:
                self.rpn.append(self.stack.pop())
            else:
                break

        self.stack.append(symbol)

    def _process_comparison(self, index, symbol):
        """Process comparison."""
        self._process_number_and_constant()

        if self.stack and self.stack[-1] in COMPARISON_SYMBOLS:
            if self.expression[index - 1] == ' ':
                raise CalculatorError('unexpected whitespace', self.__return_code)
            self.stack[-1] += symbol
        else:
            while self.stack:
                self.rpn.append(self.stack.pop())

            self.stack.append(symbol)

    def _process_brackets_and_comma(self, index, symbol):
        """Process brackets and comma from expression."""
        if symbol == ',':
            self._process_number_and_constant()
            while self.stack:
                if OPERATORS[symbol].priority < OPERATORS[self.stack[-1]].priority:
                    self.rpn.append(self.stack.pop())
                else:
                    break
            self.stack.append(symbol)
        elif symbol == '(':
            if self.number:
                self._process_number_and_constant()
                self.stack.append('*')
            self._process_operator()

            for prev_symbol in reversed(self.expression[:index]):
                if prev_symbol == ' ':
                    continue
                if prev_symbol == ')':
                    self.stack.append('*')
                break

            self.stack.append(symbol)
        elif symbol == ')':
            self._process_number_and_constant()
            while self.stack:
                element = self.stack.pop()
                if element == '(':
                    break
                self.rpn.append(element)

    def _is_unary_operator(self, index, symbol):
        """Define that operator is unary."""
        if symbol not in UNARY_OPERATORS:
            return False
        if index == 0:
            return True
        if index <= len(self.expression):
            for prev_symbol in reversed(self.expression[:index]):
                if prev_symbol == ' ':
                    continue
                elif (prev_symbol in OPERATORS and prev_symbol != ')'
                      or prev_symbol in COMPARISON_SYMBOLS):
                    return True
                else:
                    break
        return False

    def _is_floordiv(self, index, symbol):
        """Define that operator is flordiv."""
        if index <= len(self.expression):
            return symbol == self.expression[index - 1] == '/'
        return False

    def _process_expression(self):
        """Process expression to reverse polish notation."""
        for index, symbol in enumerate(self.expression):

            if self.operator in CONSTANTS:
                self._process_number_and_constant()

            if symbol in COMPARISON_SYMBOLS:
                self._process_comparison(index, symbol)
                continue

            if symbol.isdigit() and self.operator:
                self.operator += symbol
            elif symbol.isdigit() or symbol == '.':
                self._process_digit(index, symbol)
            elif symbol in ('(', ',', ')'):
                self._process_brackets_and_comma(index, symbol)
            elif symbol in OPERATORS:
                if self.stack and self._is_floordiv(index, symbol):
                    self.stack[-1] += symbol
                    continue

                if self._is_unary_operator(index, symbol):
                    self.unary_operator = UNARY_OPERATORS[symbol]
                    continue

                self._process_number_and_constant()
                self._process_stack(symbol)
            elif symbol.isalpha() or symbol == '=':
                self.operator += symbol

        self._process_number_and_constant()
        self.rpn.extend(reversed(self.stack))

        if not self.rpn:
            raise CalculatorError('not enough data to calculate', self.__return_code)

        del self.stack[:]

    def _calculate_operator(self, operator):
        """Prepare operator to calculate."""
        operator_params = OPERATORS[operator]

        real_params_count = operator_params.params_quantity
        if real_params_count == 3:
            if self.stack and self.stack[-1] == ',':
                self.stack.pop()
                real_params_count = 2
            else:
                real_params_count = 1

        if len(self.stack) < real_params_count:
            raise CalculatorError("not enough operand's for function {}".format(operator), self.__return_code)
        elif self.stack and not isinstance(self.stack[-1], (int, float)):
            raise CalculatorError("incorrect operand's for function {}".format(operator), self.__return_code)

        if real_params_count == 1:
            operand = self.stack.pop()
            self._calculate_result(operator_params.function, operand)
        elif real_params_count == 2:
            second_operand = self.stack.pop()
            first_operand = self.stack.pop()
            self._calculate_result(operator_params.function, first_operand, second_operand)

    def _calculate_result(self, function, first_operand, second_operand=None):
        """Calculate function."""
        try:
            if second_operand is None:
                result = function(first_operand)
            else:
                result = function(first_operand, second_operand)
        except ZeroDivisionError as e:
            raise CalculatorError(e, self.__return_code)
        except ArithmeticError as e:
            raise CalculatorError(e, self.__return_code)
        except Exception as e:
            raise CalculatorError(e, self.__return_code)
        else:
            self.stack.append(result)

    def _calculate_rpn(self):
        """Calculate reverse polish notation."""
        print(self.rpn)
        for item in self.rpn:
            if item == ',':
                self.stack.append(item)
            elif item in UNARY_OPERATORS.values():
                unary_operator = self._replace_unary_operator(item)
                self.stack.append(self._convert_to_number('{}1'.format(unary_operator)))
                self._calculate_operator('*')
            elif item in OPERATORS:
                self._calculate_operator(item)
            else:
                self.stack.append(item)

    def _replace_unary_operator(self, unary_operator):
        """Replace unary operator from raw expression."""
        for key, value in UNARY_OPERATORS.items():
            if value == unary_operator:
                return key

    def _convert_to_number(self, number):
        """Convert number characters to number."""
        if not isinstance(number, str):
            return 0
        return float(number) if '.' in number else int(number)

    def calculate(self):
        """Prepare and calculate expression."""
        preprocessor = Preprocessor(self.expression)
        self.expression = preprocessor.preprocessing()
        self._process_expression()
        self._calculate_rpn()

        return self.stack[-1]
