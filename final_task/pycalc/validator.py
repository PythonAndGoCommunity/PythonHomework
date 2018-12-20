import re


class Validator:
    spaces_reg = '\s+'
    sign_arr = ['<', '>', '=', '!', '/']

    @staticmethod
    def normalize_string(str):
        ''' Method that normalize string with expression. If we have more than one space between symbol,
            it change multiply spaces with one space.
            :param str: String with a math expression.
            :return : Normalized string with a math expression.
        '''
        return re.sub(Validator.spaces_reg, ' ', str).strip()

    @staticmethod
    def pre_tokinaze(str):
        ''' Method that do a number of operations before tokenization.
            :param str: String with a math expression.
            :return : Amended string with a math expression.
        '''
        str.lower()
        if Validator.par_check(str):
            normalize_str = Validator.normalize_string(str)
            valid_string = Validator.validate_string(normalize_str).replace(" ", "")
            return valid_string
        else:
            raise ValueError('Brackets not balanced')

    @staticmethod
    def par_check(expression):
        ''' Method that check for validity of brackets.
            :param expression: String with math expression.
            :return : True or False, depends on validity of brackets of a given expression.
        '''
        mapping = dict(zip('({[', ')}]'))
        queue = []
        for letter in expression:
            if letter in mapping:
                queue.append(mapping[letter])
            elif letter not in mapping.values():
                continue
            elif not (queue and letter == queue.pop()):
                return False
        return not queue


    @staticmethod
    def validate_string(str):
        ''' Method that raise error if string with a math expression is not valid.
            :param str: String with a math expression.
            :return : string with a math expression if it is valid.
        '''
        indices = enumerate(str)
        for i, char in indices:
            if char in Validator.sign_arr:
                if str[i + 1] == ' ' and str[i + 2] == '=':
                    raise ValueError('invalid syntax')
                elif char == '/' and str[i + 1] == ' ' and str[i + 2] == '/':
                    raise ValueError('invalid syntax')
            elif char.isdigit() and i != len(str) - 1:
                if str[i + 1] == ' ' and str[i + 2].isdigit():
                    raise ValueError('invalid syntax')
        return str


