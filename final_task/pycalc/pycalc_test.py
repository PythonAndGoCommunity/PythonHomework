import unittest
try:
    from pycalc import set_user_mod, postfix_translator, postfix_eval
except Exception as err:
    from .pycalc import set_user_mod, postfix_translator, postfix_eval

from math import pow, sin


class TestPostfixTranslator(unittest.TestCase):

    def setUp(self):
        set_user_mod(['math'])

    def test_common(self):
        self.assertEqual(postfix_translator("1+2*(3+4)/5.1"), "1 2 3 4 + * 5.1 / +")

    def test_pow(self):
        self.assertEqual(postfix_translator("2^2^2^2"), "2 2 2 2 ^ ^ ^")

    def test_unary_opr(self):
        self.assertEqual(postfix_translator("+-1-(-1)*-2"), "1 +- 1 +- 2 +- * -")

    def test_const(self):
        self.assertEqual(postfix_translator("pi*e-pi"), "pi e * pi -")

    def test_func(self):
        self.assertEqual(postfix_translator("pow(3,2)"), "3  2 pow(2)")

    def test_twice_opr(self):
        self.assertEqual(postfix_translator("3//2>=2!=3"), "3 2 // 2 >= 3 !=")

    def test_impl_mult(self):
        self.assertEqual(postfix_translator("(1+2)(2+3)pie"), "1 2 + 2 3 + * pi * e *")


class TestPostfixEval(unittest.TestCase):

    def setUp(self):
        set_user_mod(['math'])

    def test_common(self):
        ans = 1+2*(3-4)/5.1 % 2//2.45
        self.assertEqual(postfix_eval("1 2 3 4 - * 5.1 / 2 % 2.45 // +"), ans)

    def test_bool(self):
        ans = 3 == 1 <= 2 > 4
        self.assertEqual(postfix_eval("3 1 2 <= == 4 >"), ans)

    def test_func(self):
        ans = pow(4, 2)*sin(3)*abs(-3)
        self.assertEqual(postfix_eval("4 2 pow(2) 3 sin(1) *  3 +- abs(1) *"), ans)


if __name__ == '__main__':
    unittest.main()
