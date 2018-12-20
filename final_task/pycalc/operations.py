import math
import operator
import sys

MATHEXP_LITERAL = 0
MATHEXP_FUNCTION = 1
MATHEXP_OPERATOR = 2

COMPARISON = {
    ">=": operator.ge,
    "<=": operator.le,
    "!=": operator.ne,
    "==": operator.eq,
    "<": operator.lt,
    ">": operator.gt
}

TOKEN_TYPE_STRING = [
    "MATHEXP_LITERAL",
    "MATHEXP_FUNCTION",
    "MATHEXP_OPERATOR"
]

FUNCTION_LIST = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log,
    "log10": math.log10,
    "abs": abs,
    "round": round,
}


def get_function(exp):
    """Checks if the expression first operation should be a function"""
    for function in FUNCTION_LIST.keys():
        if exp.startswith(function + "(") and exp.endswith(")"):
            exp = exp[len(function)+1:-1]
            if parens_are_balanced(exp):
                return function
    return None


OPERATOR_PRIORITY = {
    "^": -1,
    "pow": -1,
    "*": -2,
    "//": -2,
    "/": -2,
    "%": -2,
    "+": -3,
    "-": -3
}

VARIABLES = {
    "e": math.e,
    "pi": math.pi
}


def remove_extra_parens(exp):
    """Checks if there are unneeded extra pairs of parentheses and
    removes them."""
    while exp.startswith("(") and exp.endswith(")") and\
            parens_are_balanced(exp[1:-1]):
        exp = exp[1:-1]
    return exp


def parens_are_balanced(exp):
    """Checks for any imbalance in parentheses"""
    i = 0
    for char in exp:
        if char == "(":
            i += 1
        if char == ")":
            i -= 1
        if i < 0:
            return False
    return i == 0


def evaluate_operator(token, arg1, arg2):
    if token == "^":
        return arg1 ** arg2
    if token == "*":
        return arg1 * arg2
    if token == "//":
        return arg1 // arg2
    if token == "/":
        return arg1 / arg2
    if token == "%":
        return arg1 % arg2
    if token == "+":
        return arg1 + arg2
    if token == "-":
        return arg1 - arg2
    raise Exception("ERROR: Can't find operator")


def is_operator(token):
    return token in ['^', '*', '//', '/', '%', '+', '-']


def exp_check(exp):
    if not parens_are_balanced(exp):
        print("ERROR: Brackets is not balanced")
        sys.exit(-1)
    exp = exp.replace(" ", "")
    exp = remove_extra_parens(exp)
    first = exp[0]
    last = exp[-1]
    if is_operator(first) and first != "+" and first != "-":
        print("ERROR: Expression is malformed")
        sys.exit(-1)
    if is_operator(last):
        print("ERROR: Expression is malformed")
        sys.exit(-1)
    if exp[0] == "-":
        exp = "0" + exp
    if exp[0] == "+":
        exp = exp[1:]
    return exp


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def lookup_top_operator(exp):
    pos = -1
    level = 0
    i = -1
    for token in exp:
        i += 1
        if token == "(":
            level += 1
            continue
        if token == ")":
            level -= 1
            continue
        if not is_operator(token):
            continue
        if level != 0:
            continue
        if i == 0 or i == len(exp) - 1:
            continue
        if (token == "+" or token == "-") and is_operator(exp[i - 1]):
            continue
        if pos == -1:
            pos = i
            continue
        if OPERATOR_PRIORITY[token] <= OPERATOR_PRIORITY[exp[pos]]:
            pos = i
    return pos


def is_inequality(expression):
    for i in COMPARISON:
        if expression.find(i) != -1:
            return True
    return False


def solve_inequality(expression):
    for i in COMPARISON:
        if expression.find(i) != -1:
            tmp_expr = expression.split(i)
            if tmp_expr[1] or tmp_expr[2] is None:
                print("ERROR: inequality is wrong")
                sys.exit(-1)
            a = MathExp(tmp_expr[0])
            b = MathExp(tmp_expr[1])
            return COMPARISON[i](a.evaluate(), b.evaluate())


def is_pow(expression):
    k = 0
    times = expression.count("pow", 0, len(expression))
    while k < times:
        tmp_index = expression.find("pow")
        if tmp_index != -1:
            tmp_index += 4
            arg1 = expression[tmp_index:expression.find(","):1]
            balance = 0
            i = expression.find(',')+1
            while i < len(expression):
                if expression[i] == '(':
                    balance += 1
                if expression[i] == ')':
                    balance -= 1
                if balance == -1:
                    break
                else:
                    i += 1
            arg2 = expression[expression.find(',')+1:i:1]
            tmp_index -= 4
            expression = expression.replace(
                expression[tmp_index:i+1:1], arg1+"^"+arg2)
            k += 1
    return expression


def is_logwith2args(expression):
    k = 0
    times = expression.count("log", 0, len(expression))
    while k < times:
        tmp_index = expression.find("log")
        if tmp_index != -1:
            tmp_index += 4
            arg1 = expression[tmp_index:expression.find(","):1]
            balance = 0
            i = expression.find(',') + 1
            while i < len(expression):
                if expression[i] == '(':
                    balance += 1
                if expression[i] == ')':
                    balance -= 1
                if balance == -1:
                    break
                else:
                    i += 1
            arg2 = expression[expression.find(',') + 1:i:1]
            tmp_index -= 4
            expression = expression.replace(
                expression[tmp_index:i + 1:1],
                "log("+arg1 + ")" + "/" + "log(" + arg2 + ")")
            k += 1
    return expression


class MathExp:
    """Expression parser class"""
    def __init__(self, exp):
        """The mathematical expression must be a string,
           and always must be part of the constructor."""
        self.variables_table = VARIABLES
        exp = exp_check(exp)
        function = get_function(exp)
        if function is not None:
            self.token = function
            self.left = None
            arg = exp[len(self.token)+1:-1]
            self.right = MathExp(arg)
            self.typ = MATHEXP_FUNCTION
            return
        top_operator_pos = lookup_top_operator(exp)
        if top_operator_pos >= 0:
            self.token = exp[top_operator_pos]
            self.typ = MATHEXP_OPERATOR
            exp_izq = exp[:top_operator_pos]
            exp_der = exp[top_operator_pos + 1:]
            self.left = MathExp(exp_izq)
            self.right = MathExp(exp_der)
            return
        self.token = exp
        self.typ = MATHEXP_LITERAL
        self.left = None
        self.right = None

    def evaluate(self, tmp_variables_table=None):
        """tmp_variables_table is a dict containing str:
           floar pairs, and overrides the object's own variable table"""
        if tmp_variables_table is None:
            tmp_variables_table = self.variables_table
        if self.typ == MATHEXP_LITERAL:
            if is_number(self.token):
                res = float(self.token)
                return res
            if self.token not in tmp_variables_table:
                raise Exception(
                    "ERROR: Symbol: " + self.token + "is undefined")
            res = float(tmp_variables_table[self.token])
            return res
        if self.typ == MATHEXP_FUNCTION:
            arg = self.right.evaluate(tmp_variables_table)
            res = FUNCTION_LIST[self.token](arg)
            return res
        if self.typ == MATHEXP_OPERATOR:
            left_value = self.left.evaluate(tmp_variables_table)
            right_value = self.right.evaluate(tmp_variables_table)
            res = evaluate_operator(self.token, left_value, right_value)
            return res
        sys.exit(-1)
