import math
import argparse

constants = {
    "e": math.e,
    "pi": math.pi
}

comparison = {
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
    "!=": lambda x, y: x != y,
    "==": lambda x, y: x == y
}

signs = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: x % y,
    "//": lambda x, y: x // y,
    "^": lambda x, y: x ** y
}

functions = {
    "abs": abs,
    "round": round,
    "acosh": math.acosh,
    "asinh": math.asinh,
    "atanh": math.atanh,
    "acos": math.acos,
    "asin": math.asin,
    "atan": math.atan,
    "cosh": math.cosh,
    "sinh": math.sinh,
    "tanh": math.tanh,
    "factorial": math.factorial,
    "log10": math.log10,
    "log2": math.log2,
    "cos": math.cos,
    "sin": math.sin,
    "tan": math.tan,
    "exp": math.exp,
    "sqrt": math.sqrt,
    "log": lambda x, y = math.e: math.log(x, y),
    "pow": lambda x, y: x ** y
}

priority = {
    "+": 0,
    "-": 0,
    "*": 1,
    "/": 1,
    "%": 1,
    "//": 1,
    "^": 2
}


class BracketsNotBalancedException(Exception):
    pass


class UnknownFunctionException(Exception):
    pass


class UnknownElementException(Exception):
    pass


class UnexpectedSpaceExeption(Exception):
    pass


class EmptyExpressionException(Exception):
    pass


class MissingArgumentException(Exception):
    pass


class FunctionCalculatingException(Exception):
    pass


def is_float(string):
    """Check is string float"""
    try:
        float(string)
        return True
    except ValueError:
        return False


def replace_long_unaries(expression):
    """Replaces '-' and '+' signs to one '+' or '-' sign, if there are more then one of them"""
    number_of_minuses = 0
    number_of_symbols = 0
    start = -1
    is_unar = False
    end = -1
    result_expression = expression
    for i in range(len(result_expression)):
        if result_expression[i] == "+" or result_expression[i] == "-":
            if not is_unar:
                start = i
                is_unar = True
            if result_expression[i] == "-":
                number_of_minuses += 1
            number_of_symbols += 1
        elif start != -1 and number_of_symbols > 1:
            end = i
            if number_of_minuses % 2:
                result_expression = result_expression.replace(
                    result_expression[start:end], "-")
                result_expression = replace_long_unaries(result_expression)
                break
            else:
                result_expression = result_expression.replace(
                    result_expression[start:end], "+")
                result_expression = replace_long_unaries(result_expression)
                break
        elif number_of_symbols == 1:
            start = -1
            is_unar = False
            number_of_minuses = 0
            number_of_symbols = 0
    if start != -1 and end == -1:
        raise MissingArgumentException(
            "Not enough argumets for binary operation")
    return result_expression


def checking_and_solving_comparison(expression):
    """
    Checks the expression for the presence of comparison and solves it if it is
    Parameters
    ----------
    expression : str
        The expression that is searched for comparison
    Returns
    -------
    str
        Resolved comparison if there was a comparison or expression unchanged if there no comparison
    boolean
        Is the expression comparison
    """
    is_comparison = False
    for i in range(len(expression)):
        if comparison.get(expression[i]) is not None:
            is_comparison = True
            if comparison.get(expression[i]+expression[i+1]) is not None:
                return [comparison[expression[i]+expression[i+1]](calc(expression[0:i]),
                                                                  calc(expression[i+2:len(expression)])), is_comparison]
            else:
                return [comparison[expression[i]](calc(expression[0:i]),
                                                  calc(expression[i+1:len(expression)])), is_comparison]
        elif i+1 < len(expression) and comparison.get(expression[i]+expression[i+1]) is not None:
            is_comparison = True
            return [comparison[expression[i]+expression[i+1]](calc(expression[0:i]),
                                                              calc(expression[i+2:len(expression)])), is_comparison]
    return [expression, is_comparison]


def find_left_element(expression, pointer):
    """
    Find nearest element from the left to a pointer
    Parameters
    ----------
    expression : str
        The expression that is searched for element
    pointer : int
        Position to start searching
    Returns
    -------
    str
        Nearest element from the left to a pointer
    int
        Start position of element 
    """
    first_number = ""
    start = 0
    for i in range(1, pointer+1):
        prev = first_number
        first_number = expression[pointer-i]+first_number
        if not is_float(first_number):
            first_number = prev
            start = pointer-i+1
            break
        elif expression[pointer-i] == '+' or expression[pointer-i] == '-':
            if pointer-i-1 >= 0 and (expression[pointer-i-1].isdigit() or expression[pointer-i-1] == ")"):
                first_number = prev
                start = pointer-i+1
                break
            else:
                start = pointer-i
                break
    return [first_number, start]


def find_right_element(expression, pointer):
    """
    Find nearest element from the right to a pointer
    Parameters
    ----------
    expression : str
        The expression that is searched for element
    pointer : int
        Position to start searching
    Returns
    -------
    str
        Nearest element from the right to a pointer
    int
        End position of element 
    """
    end = 0
    flag = False
    second_number = ""
    for i in range(pointer+1, len(expression)):
        prev = second_number
        second_number += expression[i]
        if second_number == '-':
            continue
        elif not is_float(second_number):
            flag = True
            second_number = prev
            end = i-1
            break
    if not flag:
        end = i
    return [second_number, end]


def calc_by_position_of_sign(position, expression):
    """
    Calculates two nearest elements (from the left and right) according to a sign at 'position'
    Parameters
    ----------
    expression : str
        The expression that is calculated
    position : int
        Position of sign in expression
    Returns
    -------
    str
        Result of calculation
    int
        Start position of left element
    int
        End of right element
    """
    if position == 0:
        raise MissingArgumentException(
            "Not enough argumets for binary operation")
    right_pointer = position
    left_pointer = position
    if position+1 == len(expression):
        raise MissingArgumentException(
            "Not enough argumets for binary operation")
    if signs.get(expression[position]+expression[position+1]) is not None:
        right_pointer = position+1
    elif signs.get(expression[position]+expression[position-1]) is not None:
        left_pointer = position-1
    [first_number, start] = find_left_element(expression, left_pointer)
    [second_number, end] = find_right_element(expression, right_pointer)
    if first_number == "" or second_number == "":
        raise MissingArgumentException(
            "Not enough argumets for binary operation")
    if left_pointer == right_pointer:
        return [signs[expression[position]](float(first_number), float(second_number)), start, end]
    else:
        return [signs["//"](float(first_number), float(second_number)), start, end]


def calc_string(expression):
    """
    Calculates expression, consisting of float numbers and signs of operations
    Parameters
    ----------
    expression : str
        The expression that is calculated
    Returns
    -------
    float
        Result of calculation
    """
    if is_float(expression):
        return float(expression)
    maxprior = -1
    position = 0
    for i in range(0, len(expression)):
        if (expression[i] == '-' or expression[i] == '+') and i == 0:
            continue
        if expression[i] in ('+', '-', '*', '/', '^', '%') and priority[expression[i]] > maxprior:
            position = i
            maxprior = priority[expression[i]]
        elif expression[i] in ('+', '-', '*', '/', '^', '%') and maxprior == 2 and priority[expression[i]] >= maxprior:
            position = i
            maxprior = priority[expression[i]]
    result = calc_by_position_of_sign(position, expression)
    new_string = expression.replace(
        expression[result[1]:result[2]+1], str("{:.16f}".format(result[0])))
    return calc_string(new_string)


def find_and_replace_consts(expression):
    """Replaces constatnts in the 'expression'"""
    if is_float(expression):
        return expression
    temp_expression = expression
    for i in constants:
        temp_expression = temp_expression.replace(i, str(constants[i]))
    return temp_expression


def add_implicit_mult(expression):
    """Adds multiplication sign where it is given implicitly"""
    result_expression = expression
    expr_left = ""
    expr_right = ""
    was_float = False
    was_const = False
    for i in range(len(result_expression)):
        expr_right += result_expression[i]
        if result_expression[i] in ("+", "-", "*", "^", "=", ">", "<", "!", "/", "(", ")", ","):
            if result_expression[i] == ")" and i+1 < len(result_expression):
                if not result_expression[i+1] in ("+", "-", "*", "^", "=", ">", "<", "!", "/", ")", ","):
                    result_expression = result_expression[0:i+1] + \
                        "*"+result_expression[i+1:len(result_expression)]
            expr_left = expr_right
            expr_right = ""
            was_const = False
            was_float = False
            if result_expression[i] == "(" and is_float(expr_left[0:len(expr_left)-1]):
                result_expression = result_expression[0:i] + \
                    "*"+result_expression[i:len(result_expression)]
        elif is_float(expr_right):
            was_float = True
        elif not is_float(expr_right) and was_float:
            result_expression = result_expression[0:i] + \
                "*"+result_expression[i:len(result_expression)]
            was_float = False
        elif constants.get(expr_right) is not None:
            was_const = True
        elif constants.get(expr_right) is None and was_const:
            is_func = False
            temp = expr_right
            for j in range(i+1, len(result_expression)):
                if functions.get(temp) is not None:
                    is_func = True
                    break
                temp += result_expression[j]
            if not is_func:
                result_expression = result_expression[0:i] + \
                    "*"+result_expression[i:len(result_expression)]
                was_const = False
    return result_expression


def solve_bracets(expression):
    """Repalces expression in brackets on it's value"""
    result_string = expression
    start = -1
    brackets_balance = 0
    for i in range(len(expression)):
        if expression[i] == '(':
            if brackets_balance == 0:
                start = i
            brackets_balance += 1
        elif expression[i] == ')':
            brackets_balance -= 1
        if start != -1 and brackets_balance == 0:
            end = i
            result_string = result_string.replace(
                result_string[start:end+1], str("{:.16f}".format(calc(result_string[start+1:end]))))
            result_string = solve_bracets(result_string)
            break
    if brackets_balance != 0:
        raise BracketsNotBalancedException("brackets not balanced")
    return result_string


def solve_functions(expression):
    """Findes and replaces functions to it's value. Solves expression in arguments, if it is necessary"""
    res_str = expression
    is_func = False
    brackets_balance = 0
    temp = ""
    end = 0
    first_end = end
    for i in range(len(expression)):
        if not (res_str[i].isdigit() or res_str[i] in (".", '+', '-', '*', '/', '^', '%', ')', '(')):
            if not is_func:
                func_start = i
            is_func = True
            temp += res_str[i]
        elif not res_str[i] in (".", '+', '-', '*', '/', '^', '%', ')', '(') and is_func:
            temp += res_str[i]
        elif res_str[i] == '(' and is_func:
            if functions.get(temp) is not None:
                start = i+1
                for j in range(i, len(expression)):
                    if expression[j] == '(':
                        brackets_balance += 1
                    elif expression[j] == ',' and brackets_balance == 1:
                        first_end = j
                    elif expression[j] == ')':
                        brackets_balance -= 1
                    if brackets_balance == 0:
                        end = j
                        break
                if first_end:
                    try:
                        res_str = res_str.replace(res_str[func_start:end+1],
                                                  str("{:.16f}".format(functions[temp](calc(res_str[start:first_end]), calc(res_str[first_end+1:end])))))
                        res_str = solve_functions(res_str)
                        break
                    except Exception:
                        raise FunctionCalculatingException(f"Incorrect arguments in function '{temp}'")
                else:
                    try:
                        res_str = res_str.replace(res_str[func_start:end+1],
                                                  str("{:.16f}".format(functions[temp](calc(res_str[start:end])))))
                        res_str = solve_functions(res_str)
                        break
                    except Exception:
                        raise FunctionCalculatingException(f"Incorrect arguments in function '{temp}'")
            else:
                raise UnknownFunctionException(f"Unknown function '{temp}'")
        elif res_str[i] in (".", '+', '-', '*', '/', '^', '%'):
            temp = ""
            is_func = False
    if temp != "" and functions.get(temp) is None and constants.get(temp) is None:
        raise UnknownElementException(f"Unknown element '{temp}'")
    return res_str


def replace_spaces(expression):
    """Findes and removes unenecessary spaces near signs"""
    result_expression = expression
    space_pos = result_expression.find(" ")
    while space_pos != -1:
        if space_pos-1 >= 0 and result_expression[space_pos-1] in ("+", "-", "*", "^", "=", ">", "<", "!", "/", ","):
            if space_pos+1 < len(result_expression) and result_expression[space_pos+1] in ("*", "^", "=", ">", "<", "!", "/"):
                raise UnexpectedSpaceExeption(f"Unexpected space between '{result_expression[space_pos-1]}' and '{result_expression[space_pos+1]}'")
            else:
                result_expression = result_expression.replace(
                    result_expression[space_pos], "", 1)
        elif space_pos+1 < len(result_expression) and result_expression[space_pos+1] in ("+", "-", "*", "^", "=", ">", "<", "!", "/"):
            if space_pos-1 >= 0 and result_expression[space_pos-1] in ("+", "-", "*", "^", "=", ">", "<", "!", "/"):
                raise UnexpectedSpaceExeption(f"Unexpected space between '{result_expression[space_pos-1]}' and '{result_expression[space_pos+1]}'")
            else:
                result_expression = result_expression.replace(
                    result_expression[space_pos], "", 1)
        else:
            raise UnexpectedSpaceExeption("Unexpected space")
        space_pos = result_expression.find(" ")
    return result_expression


def calc(expression):
    """Calculate expression with no spaces"""
    result_expression = expression
    result_expression = replace_long_unaries(result_expression)
    result_expression = solve_functions(result_expression)
    result_expression = replace_long_unaries(result_expression)
    result_expression = solve_bracets(result_expression)
    result_expression = replace_long_unaries(result_expression)
    result_expression = find_and_replace_consts(result_expression)
    result_expression = replace_long_unaries(result_expression)
    return calc_string(result_expression)


def main():
    """Main function, that parse arguments and gives the result of calculation"""
    parser = argparse.ArgumentParser(
        description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    string = parser.parse_args()
    try:
        expression = string.EXPRESSION
        expression = replace_spaces(expression)
        expression = add_implicit_mult(expression)
        [expression, is_comparison] = checking_and_solving_comparison(
            expression)
        if is_comparison:
            print(expression)
        else:
            print(calc(expression))
    except Exception as e:
        print (f"ERROR: {e}")
        return e

if __name__ == "__main__":
    main()
