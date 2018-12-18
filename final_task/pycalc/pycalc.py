import argparse
import math
import operator
import importlib.util
from sys import path


class Calc:
    """
    Class for cmd evaluating. Contains methods and Attributes for converting a mathematical expression to Reverse
    Polish Entry and its calculation.
    Attributes:
        const -> dict - contains math constant values
        func -> dict - contains tuples from math funcs and priority 4
        bin_op -> dict - contains tuples from binary funcs and their priority
        cmp -> dict - contains compare operations
        users_mod -> dict - user modules

        eval_list -> list - contains reverse polish entry
        op_st -> list - operations stack
        cmp_op -> list - contains compare operations from Expression to evaluate

        implicit_mul -> bool - flag of implicit multiplication
        
        lim -> int - length limit of operation names
    Methods:
        evaluate_expression(self, st) - evaluate Expression and return value or bool
        make_note(self, st, impl=False) - make reverse polish entry and write it to eval_list
        eval_not(self) - evaluate RPE using eval_list as source
    """
    const = {attr: getattr(math, attr) for attr in dir(math) if '_' not in attr and not callable(getattr(math, attr))}
    func = {'round': (round, 4), 'abs': (abs, 4)}

    user_modules = {}
    bin_op = {'+': (operator.add, 1), '-': (operator.sub, 1), '*': (operator.mul, 2),
              '/': (operator.truediv, 2), '%': (operator.mod,  2), '$': (operator.floordiv, 2), '^': (operator.pow, 3)}
  
    cmp = {'==': operator.eq, '<=': operator.le, '>=': operator.ge,
           '<': operator.lt, '>': operator.gt, '!=': operator.ne}

    eval_list = []  # список ОПЗ
    op_st = []  # стек с операциями

    unary = True
    implicit_mul = False    # флаг на случай неявного умножения "(2+3)4"

    # лимит на длину буквенного выражения. Если его превысить -> raise ValueError
    lim = max([len(i) for i in dir(math) if '_' not in i])

    # список операторов сравнения, если такие будут в выражении
    cmp_in_expr = []

    def __init__(self, modules):
        if modules:
            for mod in [mod + '.py' for mod in modules if '.py' not in mod]:
                for p in path:
                    try:
                        spec = importlib.util.spec_from_file_location('', location=p + r'\\' + mod)
                        foo = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(foo)
                    except:
                        raise Exception('module {} not found or cannot be loaded!'.format(mod))
                    else:
                        self.user_modules[foo] = dir(foo)

    def evaluate_expression(self, expr):
        """
        Gets string with math expression and returns result of the expression.
        The definition of comparison occurs in this function. In this case, expression will be divided into parts.
        Result of evaluating of this parts will be compared.
        :param expr: str
        :return: int, float or bool value
        """
        for key in self.cmp.keys():
            if key in expr:
                self.cmp_in_expr.append(self.cmp[key])
                expr = expr.replace(key, ' ')
        if not self.cmp_in_expr:
            self.make_note(expr)          # сборка ОПЗ
            return self.eval_note()       # вычисление ОПЗ
        else:
            expr_list = expr.split(' ')   # разбиение строки выражения на подстроки
            res = []
            for string in expr_list:
                self.make_note(string)              # сборка ОПЗ
                res.insert(0, self.eval_note())     # вычисление ОПЗ
                self.eval_list = []
            for cmp_operator in self.cmp_in_expr:
                if not cmp_operator(res[1], res[0]):
                    return False
                del res[0]
            return True

    def make_note(self, expr, impl=False):
        """
        Gets string with math expression(without compare) and stores Reverse Polish Entry in self.eval_list.
        Optional parameter 'impl' used to handle implicit multiplications using recursion.
        :param expr: str
        :param impl: bool
        :return None
        """
        self.unary = True
        self.implicit_mul = False
        temp_func = ''     # содержит не числовое выражение
        temp_num = ''      # содержит числовое выражение
        index = -1         # индекс текущего символа в выражении. Необходим для определения схожих функций(log vs log10)
        for char in expr:
            index += 1
            # формируем строку с числом если текущий элемент - цифра
            if not temp_func and char.isdigit() or char == '.':
                if self.implicit_mul is True:   # между цифрой и предыдущем элементом есть неявное умножение
                    self.make_note('*', True)
                temp_num += char
            else:                               # текущий элемент не цифра
                if temp_num:                    # заносим сформированное число в выходной лист ОПЗ
                    self.unary = False
                    self.check_num(temp_num)
                    temp_num = ''
                    # после числа неявное умножение
                    if char not in self.bin_op.keys() and char != ')' and char != ',' and char != '.':
                            self.make_note('*', True)
                else:
                    if self.unary:
                        if char == '-':
                            self.op_st.insert(0, (operator.neg, 4))
                            temp_func = ''
                            continue
                        elif char == '+':
                            self.op_st.insert(0, (operator.pos, 4))
                            temp_func = ''
                            continue

                if char == ',':    # функция round через ',' может получить второй параметр
                    self.unload_stack(True)
                    continue
                    
                # формируем строку с буквами - sin/pi/epi и тд. Из этого потом сформируем функции или const
                temp_func += char

                # попытка вытащить текущий egg из пользовательского модуля
                for module_name, module_attributes in self.user_modules.items():
                    if temp_func in module_attributes:                      # получилось вытащить
                        temp = getattr(module_name, temp_func)
                        if callable(temp):                                  # функция
                            self.op_st.insert(0, (temp, 4))
                        else:                                               # константа
                            self.unary = False
                            self.eval_list.append(temp)
                        temp_func = ''
                        break
                else:
                    if temp_func == '(':
                        self.unary = True
                        if self.implicit_mul is True:   # перед скобкой вставляем неявное умножение
                            self.make_note('*', True)
                        self.op_st.insert(0, (temp_func, 0))

                    elif temp_func == ')':
                        self.unload_stack()
                        self.implicit_mul = True        # после закрывающей скобки может быть неявное умножение
                        self.unary = False

                    # константа
                    elif temp_func in self.const:
                        self.unary = False
                        if self.implicit_mul is True:   # перед скобкой вставляем неявное умножение
                            self.make_note('*', True)
                        self.eval_list.append(self.const[temp_func])
                        self.implicit_mul = True

                    # выбор из math
                    elif temp_func in dir(math):
                        if self.implicit_mul:
                            self.make_note('*', True)
                        if self.find_real_func(expr[index + 1:]):
                            self.op_st.insert(0, (getattr(math, temp_func), 4))
                        else:
                            continue

                    elif temp_func in self.func:
                        self.op_st.insert(0, self.func[temp_func])

                    elif temp_func in self.bin_op:
                        if temp_func == '^' or (temp_func == '-' and self.unary is False) or temp_func == '+':
                            self.unary = True
                        i = 0
                        if self.op_st and not self.op_st[0][0] == self.bin_op[temp_func][0] == operator.pow:
                            for operation in self.op_st:          # выталкиваем приоритетные, префиксные операции
                                if operation[1] >= self.bin_op[temp_func][1]:
                                    self.eval_list.append(operation[0])
                                else:
                                    break
                                i += 1
                        self.op_st[:i] = []
                        self.op_st.insert(0, self.bin_op[temp_func])
                        self.implicit_mul = False       # наличие бинарной операции исключает неявное умножение

                    else:
                        if self.lim <= len(temp_func):
                            raise ValueError('unknown function or constant!')
                        continue
                    temp_func = ''
        if temp_func:
            raise ValueError('unknown function or constant!')
        if impl is True:    # обработка неявного умножения. Чисел нет, лист операций трогать нельзя - выход из функции
            self.implicit_mul = False
            return
        if temp_num:                                    # осталось еще число
            self.check_num(temp_num)
        for operation in self.op_st:                          # выгрузить все оставшиеся операции
            self.eval_list.append(operation[0])
        self.op_st = []

    def unload_stack(self, is_dot=False):
        self.unary = False
        for op in self.op_st:  # выгружаем все операции до открывающей скобки
            if op[0] == '(':
                self.op_st = self.op_st[self.op_st.index(op) + 1:]
                break
            self.eval_list.append(op[0])
        if is_dot:
            self.op_st.insert(0, ('(', 0))

    def check_num(self, temp_num):            # определение типа числа
        if '.' in temp_num:
            if len(temp_num) == 1:
                raise ValueError('incorrect using dots!')
            self.eval_list.append(float(temp_num))
        else:
            self.eval_list.append(int(temp_num))

    # проверка на неполноту функции(log vs log10)
    @staticmethod
    def find_real_func(remainder):
        index = remainder.index('(')
        if not index:       # функция уже полная, за ней идет скобка
            return True
        else:
            return False

    def eval_note(self):
        """
        Evaluate Reverse Polish Entry from self.evaluate_list
        :return: int or float
        """
        num_stack = []
        for i in self.eval_list:
            if not callable(i):                     # данный элемент не функция, т.е., число -> поместить в стек чисел
                num_stack.insert(0, i)
            else:                                   # операция -> применить к двум выше лежащим элементам в стеке
                try:
                    egg = i(*num_stack[1::-1])
                    num_stack[:2] = [egg]
                except TypeError as ex:
                    if '2 given' in str(ex):
                        num_stack[0] = i(num_stack[0])
                    if 'got 1' in str(ex):
                        raise Exception('incorrect expression!')

        return num_stack[0]


def calculate(expr, modules):
    combinations_for_replace = {' + ': '+', ' * ': '*', ', ': ',', ' - ': '-', ' -': '-', '\'': '', '"': ''}

    for i, r in combinations_for_replace.items():
        expr = expr.replace(i, r)
    if ' ' in expr:
        raise ValueError('spaces in expression!')
    if not expr:
        raise ValueError('empty expression!')
    if expr.count('(') != expr.count(')'):
        raise ValueError('brackets are not balanced!')
    if '$' in expr or 'q' in expr:
        raise ValueError('incorrect symbols!')
    else:
        expr = expr.replace('//', '$')
    cd = Calc(modules)
    print(cd.evaluate_expression(expr))


def parse_cmd_args():
    try:
        parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')

        parser.add_argument('EXPRESSION', help='Expression string to evaluate')
        parser.add_argument('-m', '--use-modules', action='store', nargs='*',
                            dest='modules', help='Using your own module', default=None)
        pr = parser.parse_args()
        calculate(pr.EXPRESSION, pr.modules)

    except Exception as e:
        print('ERROR: ', e, sep='\n', end='')


if __name__ == '__main__':
    parse_cmd_args()
