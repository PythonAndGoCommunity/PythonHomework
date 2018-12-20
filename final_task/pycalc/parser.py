from pycalc.operators import operators_dict, Operator, Function, Constant
from pycalc.validator import Validator
from pycalc.importmodules import FunctionParser
functions_dict = {}
const_dict = {}


class Parser:
    def __init__(self):
        self.func_parser = FunctionParser()

    @staticmethod
    def is_number(s):
        """ Returns True is string is a number. """
        if isinstance(s, Operator) or isinstance(s, Function) or isinstance(s, Constant) or s == 'pow':
            return False
        return s.replace('.', '', 1).isdigit()

    @staticmethod
    def is_operator(s):
        return s in operators_dict

    @staticmethod
    def is_function(s):
        return s in FunctionParser.functions_dict

    @staticmethod
    def is_constant(s):
        return s in FunctionParser.constants_dict

    @staticmethod
    def add_multiply_sign(lexem_list):
        for i in range(1, len(lexem_list)):
            if isinstance(lexem_list[i], Function) and not isinstance(lexem_list[i-1], Operator):
                lexem_list.insert(i, operators_dict['*'])
            elif isinstance(lexem_list[i], Function) and isinstance(lexem_list[i-1], Operator) \
                 and lexem_list[i-1].name == ')':
                lexem_list.insert(i, operators_dict['*'])
            elif isinstance(lexem_list[i], Operator) and lexem_list[i].name == '(' and \
                (isinstance(lexem_list[i-1], Constant) or Parser.is_number(lexem_list[i-1])):
                lexem_list.insert(i, operators_dict['*'])
            elif isinstance(lexem_list[i], Operator) and lexem_list[i].name == '(' and \
                isinstance(lexem_list[i-1], Operator) and lexem_list[i-1].name == ')':
                lexem_list.insert(i, operators_dict['*'])
            elif isinstance(lexem_list[i], Operator) and lexem_list[i].name == '(' and \
                not isinstance(lexem_list[i-1], Operator) and not isinstance(lexem_list[i-1], Function):
                lexem_list.insert(i, operators_dict['*'])
            elif isinstance(lexem_list[i], Constant) and isinstance(lexem_list[i-1], Constant):
                lexem_list.insert(i, operators_dict['*'])
        return lexem_list

    def parse_expression(self, exp):
        exp = Validator.pre_tokinaze(exp)
        exp.replace(" ", "")
        lexem_array = []
        start_index = 0
        end_index = len(exp)
        while start_index != len(exp):
            substring = exp[start_index:end_index]
            if Parser.is_number(substring):
                lexem_array.append(substring)
                start_index, end_index = end_index, len(exp)
            elif Parser.is_operator(substring):
                operator = operators_dict[substring]
                lexem_array.append(operator)

                start_index, end_index = end_index, len(exp)
            elif Parser.is_constant(substring):
                lexem_array.append(self.func_parser.constants_dict[substring])
                start_index, end_index = end_index, len(exp)
            elif Parser.is_function(substring):
                lexem_array.append(self.func_parser.functions_dict[substring])
                start_index, end_index = end_index, len(exp)
            else:
                end_index -= 1
        lex_list =Parser.add_multiply_sign(lexem_array)
        unary_signs = Parser.find_unary_signs(lex_list)
        final_lexem_list = Parser.remove_redundant_unary_signs(unary_signs, lex_list)

        return final_lexem_list

    @staticmethod
    def find_unary_signs(lexem_list):
        final_list = []
        for i in range(len(lexem_list)):
            if i == 0 and isinstance(lexem_list[i], Operator) and lexem_list[i].name in ['+', '-']:
                final_list.append(0)
            elif (isinstance(lexem_list[i], Operator) and lexem_list[i].name in ['+', '-']) and \
                  not (isinstance(lexem_list[i-1], Constant) or Parser.is_number(lexem_list[i-1])) \
                  and not (isinstance(lexem_list[i-1], Operator) and lexem_list[i-1].name == ')'):
                final_list.append(i)
        lexems_with_indicies = enumerate(lexem_list)
        lexems_filter = list(filter(lambda x: x[0] in final_list, lexems_with_indicies))
        for unary_sign in lexems_filter:
            lexem_list[unary_sign[0]] = operators_dict['unary_plus'] if unary_sign[1] == '+' else operators_dict['unary_minus']
        return lexems_filter

    @staticmethod
    def remove_redundant_unary_signs(lexems_with_indicies, lex_list):
        final_index = len(lexems_with_indicies)-1
        while final_index != -1:
            last_index, last_sign = lexems_with_indicies[final_index]
            prev_index, prev_sign = lexems_with_indicies[final_index - 1]
            if last_index - 1 == prev_index and last_sign.name == prev_sign.name:
               lex_list[prev_index:last_index + 1] = [operators_dict['unary_plus']]
               lexems_with_indicies[final_index - 1: final_index + 1] = [(prev_index,  operators_dict['+'])]
            elif last_index - 1 == prev_index and last_sign != prev_sign:
                lex_list[prev_index: last_index + 1] = [operators_dict['unary_minus']]
                lexems_with_indicies[final_index - 1: final_index + 1] = [(prev_index,  operators_dict['-'])]
            final_index -= 1
        return lex_list


