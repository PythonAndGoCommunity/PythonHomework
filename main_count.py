import re
import pycalc as py


def main_count(formula):

    def degreePriorityFormat(formula):

        result_formula = []

        for i, key in enumerate(formula.split('^')):
            result_formula.append(key)
            if i != len(formula.split('^')) - 1:
                result_formula.append('^' * (i + 1))
                # add in operators degree with high priority
                py.operators.update({'^' * (i + 1): (4 + i, lambda x, y: x ** y)})
                py.doubleOperators.append('^' * (i + 1))
                py.operList.append('^' * (i + 1))

        return ''.join(result_formula)

    def formatDegreeReplace(formula):

        expression = []
        count_argument = False
        count_bracket = 0
        for i, key in enumerate(formula):

            if key == '(':
                count_bracket += 1
            elif key == ')':
                count_bracket -= 1

            if count_argument:
                expression.append(key)

            if key == ')' and not count_bracket and count_argument:
                break

            if key == '^' and formula[i + 1].isalpha():
                count_argument = True
        # replace only 1 time
        formula = formula.replace("{}".format(''.join(expression)), "({})".format(''.join(expression)), 1)

        # replace other instance
        count = False
        for i, key in enumerate(formula):
            if key == '^' and formula[i + 1].isalpha():
                count = True
                break
        if count:
            formula = formatDegreeReplace(formula)

        return formula

    def negativeNumber(formula):

        expression = []
        count = False
        bracket_count = 0
        for i, key in enumerate(formula):

            if count:
                if key == ')' and not bracket_count:
                    expression.append(key)
                    break
                elif key == ')':
                    bracket_count -= 1
                elif key == '(':
                    bracket_count += 1

                if expression and (key in py.doubleOperators or key in py.compareOperators) and not bracket_count:
                    break
                else:
                    expression.append(key)

            if key == '^' and formula[i + 1] == '-':
                count = True

        # replace only first expression
        formula = formula.replace(("^{}".format(''.join(expression))), "^(0{})".format(''.join(expression)), 1)

        # replace other expressions
        if '^-' in formula:
            formula = negativeNumber(formula)

        return formula

    def reversePolConvert(splitted_formula):

        stack = []
        for token in splitted_formula:
            # replace const
            if token in py.const:
                token = py.const.get(''.join(token))

            if token in py.operators:
                # choose by priority
                while stack and stack[-1] != "(" and py.operators[token][0] <= py.operators[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def reversePolNotation(converted_formula):

        stack = []
        for token in converted_formula:

            if token in py.operators:
                # check function with double arguments
                if token in py.doubleOperators:
                    y, x = stack.pop(), stack.pop()
                    stack.append(py.operators[token][1](x, y))
                else:
                    # use function with 1 argument
                    x = stack.pop()
                    stack.append(py.operators[token][1](x))
            else:
                stack.append(token)

        return stack[0]

    def formulaFormatting(formula):

        # delete backspace
        formula = formula.replace(' ', '')
        # replace )( into )*( for readable form
        formula = formula.replace(')(', ')*(')
        # replace (- into (0- for readable form
        formula = '(0-'.join(formula.split('(-'))

        # formatting a formula with two arguments
        for name_function in ['pow', 'log(', 'copysign', 'ldexp', 'atan2', 'hypot', 'fmod', 'gcd']:
            if name_function in formula:
                # use only log (without log10,log1p)
                if name_function == 'log(':
                    name_function = 'log'
                formula = twoArgsFormat(formula, name_function)

        # find degree by function
        for i, key in enumerate(formula):
            if key == '^' and formula[i + 1].isalpha():
                formula = formatDegreeReplace(formula)
                break

        # find the number of degrees
        if formula.count("^") > 1:
            formula = degreePriorityFormat(formula)

        # replace sign "+","-" in front formula
        new_data = []
        new_data.append(formula[0])

        for token in formula[1:]:
            if new_data[-1] == '+' and token == '-':
                new_data[-1] = '-'
            elif new_data[-1] == '-' and token == '+':
                new_data[-1] = '-'
            elif new_data[-1] == '-' and token == '-':
                new_data[-1] = '+'
            elif new_data[-1] == '+' and token == '+':
                new_data[-1] = '+'
            else:
                new_data.append(token)
        if new_data[0] == '-':
            new_data.insert(0, '0')
        if new_data[0] == '+':
            new_data.pop(0)

        formula = ''.join(new_data)

        # replace negative number in formula into zero with brackets
        # replace 5/-1 into 5*(0-1)/1
        formula = formula.replace('/-', '*(0-1)/')
        formula = formula.replace('*-', '*(0-1)*')

        # replace negative number with degree in formula into zero with brackets
        if '^-' in formula:
            formula = negativeNumber(formula)

        # format function fsum because fsum([1,2,3,4..]) has many arguments
        if 'fsum' in formula:
            formula = fsum(formula)

        return formula

    def split(formatted_formula):

        stack = []
        for i, key in enumerate(formatted_formula):

            if key in '1234567890.':
                # check log10 log1p log2
                if len(stack) > 2 and ''.join(stack[:3]) == 'log':

                    stack.append(key)
                    if ''.join(stack) in py.operList:
                        yield ''.join(stack)
                        stack = []

                elif stack and (stack[0] not in '1234567890.'):
                    yield ''.join(stack)
                    stack = []
                    stack.append(key)
                else:
                    stack.append(key)

            else:
                if key in '()':
                    if stack and (stack[0] in '1234567890.'):
                        yield float(''.join(stack))
                    elif stack:
                        yield ''.join(stack)

                    stack = []
                    stack.append(key)

                elif len(stack) > 2 and ''.join(stack[:3]) == 'log':
                    stack.append(key)
                    if ''.join(stack) in py.operList:
                        yield ''.join(stack)
                        stack = []

                elif stack and stack[0] in '1234567890.':
                    yield float(''.join(stack))
                    stack = []
                    stack.append(key)

                else:

                    if ''.join(stack) + key in py.operList:
                        stack.append(key)

                    elif ''.join(stack) in py.const:
                        yield py.const.get(''.join(stack))
                        stack = []
                        stack.append(key)

                    elif ''.join(stack) in py.operList:

                        yield ''.join(stack)
                        stack = []
                        stack.append(key)
                    else:
                        stack.append(key)
        else:

            if stack and (stack[0] in '1234567890.'):
                yield float(''.join(stack))
            elif ''.join(stack) in py.const:
                yield py.const.get(''.join(stack))
            else:
                yield ''.join(stack)

    def comparisonCheck(formula):

        for compare in py.compareOperators:
            if compare in formula:
                return py.compareOperators.get(compare)(
                    main_count(formula.split(compare)[0]),
                    main_count(formula.split(compare)[1]))

        # start calculation
        return reversePolNotation(reversePolConvert(split(formulaFormatting(formula))))

    def fsum(formula):

        count_brackets = 0
        count_brackets_square = 0
        count_arguments = []
        add_argument = []

        for key in formula.split('fsum([', 1)[1:][0]:
            if key == "]" and not count_brackets_square:
                break

            if key == ',' and not count_brackets:
                count_arguments.append(''.join(add_argument))
                add_argument = []
            else:
                add_argument.append(key)

            if key == ']':
                count_brackets_square -= 1
            elif key == '[':
                count_brackets_square += 1
            elif key == ')':
                count_brackets -= 1
            elif key == '(':
                count_brackets += 1

        count_arguments.append(''.join(add_argument))

        result_count = 0
        for argument in count_arguments:
            result_count += float(main_count(argument))

        replace_expression = "fsum([{}])".format(','.join(count_arguments), 1)

        result_formula = formula.replace(replace_expression, str(result_count), 1)

        return result_formula

    def tracebackFinder (formula):
        # check error

        if not formula:
            return "ERROR: no value"
        else:

            if formula[-1] in py.operators:
                return "ERROR: syntax mistake"
            if formula[0] in '^%*/= |\\':
                return "ERROR: syntax mistake"

            if re.search(r'\d\s\d', formula):
                return "ERROR: syntax mistake"

            if formula.count('(') != formula.count(')'):
                return "ERROR: brackets are not balanced"

            if formula in py.operators:
                return "ERROR: no function arguments"

            if '()' in formula or '[]' in formula:
                return "ERROR: no function arguments"

            if re.search(r'[*,/,<,>,%,^][*,/,<,>,%,^]', formula):
                return "ERROR: syntax error in statements"

            if re.search(r'[*,/,<,>,%,^,=]\s[*,/,<,>,%,^,=]', formula):
                return "ERROR: syntax error in statements"

            if re.search(r'log[1,2][0,p][^(]', formula):
                return "ERROR: unknown function"

            # function argument checking
            for name_func in py.operators:
                if name_func.isalpha() or name_func in ['log1p', 'log10', 'atan2', 'expm1', 'log2']:
                    # split by function name + '('
                    name_func_bracket = '{}('.format(name_func)

                    if name_func_bracket in formula:

                        for expression in formula.split(name_func_bracket)[1:]:
                            count_brackets = 0
                            count_arguments = 0
                            for key in expression:
                                if key == ',' and not count_brackets:
                                    # arguments are separated by commas
                                    # count when no count_brackets
                                    count_arguments += 1

                                if key == ')' and not count_brackets:
                                    break
                                elif key == ')':
                                    count_brackets -= 1
                                elif key == '(':
                                    count_brackets += 1

                            if count_arguments > 1:
                                return "ERROR: function arguments are not balanced"
                            # function pow has two or one argument
                            elif (count_arguments > 1 or count_arguments == 0) and name_func == 'pow':
                                return "ERROR: function arguments are not balanced"
                            # these functions have 2 arguments
                            elif count_arguments == 0 and name_func in ['atan2', 'copysign', 'fmod', 'gcd', 'hypot',
                                                                        'isclose', 'ldexp', 'pow']:
                                return "ERROR: function arguments are not balanced"
                            # other functions with 1 argument
                            elif count_arguments > 0 and name_func not in ['atan2', 'copysign', 'fmod', 'gcd', 'hypot',
                                                                           'isclose', 'ldexp', 'pow', 'log']:
                                return "ERROR: function arguments are not balanced"

    def twoArgsFormat(formula, name_function):
        # two arguments formatting formula

        result_formula = formula
        first_argument = []
        second_argument = []
        count_argument = True
        count_bracket = 0

        # find first and second argument
        for key in (name_function).join(formula.split('{}'.format(name_function))[1:]):

            if key == '(':
                count_bracket += 1
            if key == ')':
                count_bracket -= 1
            if key == ',':
                first_argument.pop(0)
                count_argument = False

            if key == ')' and not count_bracket and not count_argument:
                break
            elif key == ')' and not count_bracket:
                first_argument.append(key)
                break

            elif count_argument:
                first_argument.append(key)

            else:
                if key != ',':
                    second_argument.append(key)

        # if not second argument into log - the base by log = e
        # if log(x) format into log(x,e)
        if not second_argument and name_function == 'log':
            second_argument.append('e')
            replace_expression = "{}{}".format(name_function, ''.join(first_argument), 1)
        else:
            replace_expression = "{}({},{})".format(name_function, ''.join(first_argument),
                                                    ''.join(second_argument), 1)

        # count every argument
        x = main_count(''.join(first_argument))
        y = main_count(''.join(second_argument))

        # function gcd have only int arguments
        if name_function == 'gcd':
            x = int(x)
            y = int(y)

        result_function = py.operators[name_function][1](x, y)
        # replace only 1 time
        result_formula = result_formula.replace(replace_expression, str(result_function), 1)

        # double entry check
        if name_function == 'log':
            # there are log2p, log10 with 1 argument
            if 'log(' in result_formula:
                result_formula = twoArgsFormat(result_formula, name_function)
        else:
            if name_function in result_formula:
                result_formula = twoArgsFormat(result_formula, name_function)

        return result_formula

    return tracebackFinder (formula) if tracebackFinder (formula) else comparisonCheck(formula)

