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
        users_mod -> dict - users modules

        eval_list -> list - contains reverse polish entry
        op_st -> list - operations stack
        cmp_op -> list - contains compare operations from Expression to evaluate
        
        implicit_mul -> bool - flag of implicit multiplication
        
        lim -> int - length limit of operation names
    Methods:
        __init__(self, users) - collects member names of user modules 
        my_eval(self, st) - evaluates Expression and return value or bool
        make_note(self, st, impl=False) - makes reverse polish entry and write it to eval_list
        eval_not(self) - evaluates RPE using eval_list as source
        check_num(self, temp_num) - converts str to int or float and store num in eval_list
    """
    const = {'pi': math.pi, 'e': math.e, 'q': math.pi * math.e}
    func = {'round': (round, 4), 'abs': (abs, 4)}

    users_mod = {}
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

    cmp_op = []

    def __init__(self, users: list):
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

    def my_eval(self, st: str):
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
                if not op(res[1], res[0]):
                    return False
                del res[0]
            return True

    def make_note(self, st: str, impl=False):
        self.unary = True
        self.implicit_mul = False
        egg = ''       # содержит операцию
        temp_num = ''  # содержит операнд
        for c in st:
            if c.isdigit() or c == '.':         # формируем строку с числом если текущий элемент - цифра
                if self.implicit_mul is True:   # между цифрой и предыдущем элементом есть неявное умножение
                    self.make_note('*', True)
                temp_num += c
            else:                               # текущий элемент не цифра
                if temp_num:                    # заносим сформированное число в выходной лист ОПЗ
                    self.unary = False
                    self.check_num(temp_num)
                    temp_num = ''
                    # после числа неявное умножение
                    if c not in self.bin_op.keys() and c != ')' and c != ',' and c != '.':
                            self.make_note('*', True)
                else:
                    if self.unary:
                        if c == '-':
                            self.op_st.insert(0, (operator.neg, 4))
                            egg = ''
                            continue
                        elif c == '+':
                            self.op_st.insert(0, (operator.pos, 4))
                            egg = ''
                            continue

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
                            self.unary = False
                            self.eval_list.append(temp)
                        egg = ''
                        break
                else:
                    if egg == '(':
                        self.unary = True
                        if self.implicit_mul is True:   # перед скобкой вставляем неявное умножение
                            self.make_note('*', True)
                        self.op_st.insert(0, (egg, 0))

                    elif egg == ')':
                        self.unary = False
                        for o in self.op_st:            # выгружаем все операции до открывающей скобки
                            if o[0] == '(':
                                self.op_st = self.op_st[self.op_st.index(o) + 1:]
                                break
                            self.eval_list.append(o[0])
                        self.implicit_mul = True        # после закрывающей скобки может быть неявное умножение

                    # константа
                    elif egg in self.const:
                        self.unary = False
                        self.eval_list.append(self.const[egg])
                        # self.check_neg()
                        self.implicit_mul = True

                    # выбор из math
                    elif egg in dir(math):
                        if self.implicit_mul:
                            self.make_note('*', True)
                        self.op_st.insert(0, (getattr(math, egg), 4))

                    elif egg in self.func:
                        self.op_st.insert(0, self.func[egg])

                    elif egg in self.bin_op:
                        if egg == '^' or (egg == '-' and self.unary is False):
                            self.unary = True
                        i = 0
                        if self.op_st and not self.op_st[0][0] == self.bin_op[egg][0] == operator.pow:
                            for o in self.op_st:          # выталкиваем приоритетные, префиксные операции
                                if o[1] >= self.bin_op[egg][1]:
                                    self.eval_list.append(o[0])
                                    del self.op_st[0]
                                else:
                                    break
                                i += 1
                        self.op_st[:i] = []
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
            self.check_num(temp_num)
        for o in self.op_st:                          # выгрузить все оставшиеся операции
            self.eval_list.append(o[0])
        self.op_st = []

    def check_num(self, temp_num: str):            # определение типа числа
        if '.' in temp_num:
            if len(temp_num) == 1:
                raise ValueError('incorrect using dots!')
            self.eval_list.append(float(temp_num))
        else:
            self.eval_list.append(int(temp_num))

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
                    # print(ex)
                    if '2 given' in str(ex):
                        num_stack[0] = i(num_stack[0])
                    if 'got 1' in str(ex):
                        raise Exception('incorrect expression!')

        return num_stack[0]


def calculate():
    re = {' + ': '+', ' * ': '*', ', ': ',', ' - ': '-', '\'': '', '"': ''}
    try:
        parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')

        parser.add_argument('EXPRESSION', help='Expression string to evaluate')
        parser.add_argument('-m', '--use-modules', action='store', nargs='*',
                            dest='user', help='Using your own module', default=None)
        pr = parser.parse_args().__dict__
        s = pr['EXPRESSION']

        user = []
        if pr['user']:
            user += pr['user']
        for i, r in re.items():
            s = s.replace(i, r)
        if ' ' in s:
            raise ValueError('spaces in expression!')
        if not s:
            raise ValueError('empty expression!')
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
        print('ERROR: ', e, sep='\n', end='')


if __name__ == '__main__':
    calculate()
