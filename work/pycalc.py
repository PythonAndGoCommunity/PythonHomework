import argparse
import math
import operator
import importlib.util
from sys import path


class Calc:
    """
    Pretty class for cmd evaluating
    Attributes:
        const -> dict - contains math constant values
        func -> dict - contains tuples from math funcs and priority 4
        bin_op -> dict - contains tuples from binary funcs and their priority
        cmp -> dict - contains compare operations

        eval_list -> list - contains reverse polish entry
        op_st -> list - operations stack
        cmp_op -> list - contains compare operations from Expression to evaluate
        
        implicit_mul -> bool - flag of implicit multiplication
        neg -> bool - variable negation flag
        
        lim -> int - length limit of operation names
    Methods:
        my_eval(self, st) - evaluate Expression and return value or bool
        make_note(self, st, impl=False) - make reverse polish entry and write it to eval_list
        eval_not(self) - evaluate RPE using eval_list as source
    """
    const = {'pi': math.pi, 'e': math.e, 'q': math.pi * math.e}
    func = {'round': (round, 4), 'abs': (abs, 4)}

    users_mod = {}
    
    bin_op = {'+': (operator.add, 1), '-': (operator.neg, 1), '*': (operator.mul, 2),
              '/': (operator.truediv, 2), '%': (operator.mod,  2), '$': (operator.floordiv, 2), '^': (operator.pow, 3)}
  
    cmp = {'<': operator.lt, '>': operator.gt, '==': operator.eq, '<=': operator.le, '>=': operator.ge}

    eval_list = []  # список ОПЗ
    op_st = []  # стек с операциями

    # для унарных операций. суть такова: все вычитания заменяем на сложение
    # при этом вычитатель - это просто слагаемое с минусом. На случай нескольких минусов предусмотрена сложная логика
    neg = False
    implicit_mul = False    # флаг на случай неявного умножения "(2+3)4"

    # лимит на длину буквенного выражения. Если его превысить -> raise ValueError
    lim = max([len(i) for i in dir(math) if '_' not in i])

    cmp_op = []

    def __init__(self, users):
        for u in [u + '.py' for u in users if '.py' not in u]:
            for p in path:
                try:
                    spec = importlib.util.spec_from_file_location('', location=p + r'\\' + u)
                    foo = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(foo)
                except:
                    continue
                else:
                    self.users_mod[foo] = dir(foo)

    def my_eval(self, st):
        for k in self.cmp.keys():
            if k in st:
                self.cmp_op.append(self.cmp[k])
                st = st.replace(k, ' ')
        if not self.cmp_op:
            self.make_note(st)          # сборка ОПЗ
            return self.eval_note()   # вычисление ОПЗ
        else:
            st = st.split(' ')
            res = []
            for string in st:
                self.make_note(string)              # сборка ОПЗ
                res.insert(0, self.eval_note())   # вычисление ОПЗ
                self.eval_list = []
            for op in self.cmp_op:
                if not op(res[0], res[1]):
                    return False
                del res[0]
            return True

    def make_note(self, st, impl=False):
        egg = ''       # содержит операцию
        temp_num = ''  # содержит операнд
        for c in st:
            if c.isdigit():                     # формируем строку с числом если текущий элемент - цифра
                if self.implicit_mul is True:   # между цифрой и предыдущем элементом есть неявное умножение
                    self.make_note('*', True)
                temp_num += c
            else:                               # текущий элемент не цифра
                if temp_num:                    # заносим сформированное число в выходной лист ОПЗ
                    if self.neg:                # перед этим операндом был минус
                        self.eval_list.append(-int(temp_num))
                        self.neg = False
                    else:
                        self.eval_list.append(int(temp_num))
                    temp_num = ''
                    if c not in self.bin_op.keys() and c != ')':     # после числа неявное умножение
                            self.make_note('*', True)

                if c == ',':    # функция round через ',' может получить второй параметр
                    continue

                egg += c  # формируем строку с буквами - sin/pi/epi и тд. Из этого потом сформируем функции или const
                # попытка вытащить текущий egg из пользовательского модуля
                for u, d in self.users_mod.items():
                    if egg in d:                                # получилось вытащить
                        temp = getattr(u, egg)
                        if callable(temp):                      # функция
                            self.op_st.insert(0, (temp, 4))
                        else:                                   # константа
                            self.check_neg(temp)
                        egg = ''
                        break
                else:
                    if egg == '(':
                        if self.implicit_mul is True:   # перед скобкой вставляем неявное умножение
                            self.make_note('*', True)
                        self.op_st.insert(0, (egg, 0))

                    elif egg == ')':
                        for o in self.op_st:            # выгружаем все операции до открывающей скобки
                            if o[0] == '(':
                                self.op_st = self.op_st[self.op_st.index(o) + 1:]
                                break
                            self.eval_list.append(o[0])
                        self.implicit_mul = True        # после закрывающей скобки может быть неявное умножение

                    # константа
                    elif egg in self.const:
                        self.check_neg(self.const[egg])

                    # выбор из math
                    elif egg in dir(math):
                        self.op_st.insert(0, (getattr(math, egg), 4))

                    elif egg in self.bin_op:
                        if egg == '-':                  # сложная логика для унарных отрицаний.
                            self.neg = False if self.neg else True
                            egg = '+'
                        for o in self.op_st:          # выталкиваем приоритетные, префиксные операции
                            if o[1] >= self.bin_op[egg][1]:
                                self.eval_list.append(self.op_st.pop(0)[0])
                            else:
                                break
                        self.op_st.insert(0, self.bin_op[egg])
                        self.implicit_mul = False       # наличие бинарной операции исключает неявное умножение

                    else:
                        if self.lim <= len(egg):
                            raise ValueError('unknown function or constant!')
                        continue
                    egg = ''
        if egg:
            raise ValueError('unknown function or constant!')
        if impl is True:    # обработка неявного умножения. Чисел нет, лист операций трогать нельзя - выход из функции
            self.implicit_mul = False
            return
        if temp_num:                                    # осталось еще число
            if self.neg:                                # перед этим операндом был минус
                self.eval_list.append(-int(temp_num))
                self.neg = False
            else:
                self.eval_list.append(int(temp_num))
        for o in self.op_st:                          # выгрузить все оставшиеся операции
            self.eval_list.append(o[0])

    def check_neg(self, const):                       # отрицание константы
        if self.neg:
            self.eval_list.append(-const)
            self.neg = False
        else:
            self.eval_list.append(const)
        self.implicit_mul = True                       # после константы может быть неявное умножение

    def eval_note(self):
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

        return num_stack[0]


try:
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')

    parser.add_argument('EXPRESSION', help='Expression string to evaluate')
    parser.add_argument('-m', '--use-modules', action='store', nargs='*',
                        dest='user', help='Using your own module', default=None)
    pr = parser.parse_args().__dict__
    s = pr['EXPRESSION']
    user = [] + pr['user']
    s = s.replace(' ', '')
    s = s[1:-1]
    if s.count('(') != s.count(')'):
        raise ValueError('brackets are not balanced!')
    if '$' in s or 'q' in s:
        raise ValueError('incorrect symbols!')
    else:
        s = s.replace('//', '$')
        s = s.replace('epi', 'q')
        s = s.replace('pie', 'q')
    cd = Calc(user)
    print(cd.my_eval(s))
except Exception as e:
    print('PROBLEM', e, sep='\n')
