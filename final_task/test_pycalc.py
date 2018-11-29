import unittest
import pycalc.compexp as compexp
import pycalc.calcexp as calcexp
import pycalc.expproc as expproc
import pycalc.pycalc as pycalc
import pycalc.custom_exception as custom_exc
import pycalc.parse as parse
import pycalc.dictwithmissing as dictwithmissing


class TestPycalc(unittest.TestCase):
    def test_parse_argument(self):
        self.assertEqual(parse.parse_argument(["1+2"]), "1+2")

    def test_custom_expression(self):
        error = custom_exc.VerifyError("123")
        self.assertEqual(error.msg, "123")

    def test_mydict(self):
        dict = {1: "a", 2: "b", 3: "c"}
        my_dict = dictwithmissing.DictWithMissing(dict)
        self.assertEqual(my_dict[1], "a")
        self.assertEqual(my_dict[4], -1)

    def test_check_for_comp(self):
        self.assertEqual(compexp.check_for_comp("1+2"), ["1+2"])
        self.assertEqual(compexp.check_for_comp("1>2")[0:2], ["1", "2"])
        self.assertEqual(compexp.check_for_comp("1>=2")[0:2], ["1", "2"])
        self.assertEqual(compexp.check_for_comp("1<2")[0:2], ["1", "2"])
        self.assertEqual(compexp.check_for_comp("1<=2")[0:2], ["1", "2"])
        self.assertEqual(compexp.check_for_comp("1==2")[0:2], ["1", "2"])
        self.assertEqual(compexp.check_for_comp("1!=2")[0:2], ["1", "2"])
        self.assertRaises(custom_exc.VerifyError, compexp.check_for_comp, "1>2>3")
        self.assertRaises(custom_exc.VerifyError, compexp.check_for_comp, "1>=2==3")

    def test_verify_expression(self):
        self.assertEqual(expproc.verify_expression("1+2"), "1 2 + ")
        self.assertEqual(expproc.verify_expression(".1*2.0^56.0"), ".1 2.0 56.0 ^ * ")
        self.assertEqual(expproc.verify_expression("-10-2"), "10 neg 2 - ")
        self.assertEqual(expproc.verify_expression("1 "), "1  ")
        self.assertEqual(expproc.verify_expression("2*(2+3)"), "2  2 3 +  * ")
        self.assertEqual(expproc.verify_expression("pi*e"), "pi  e  * ")
        self.assertEqual(expproc.verify_expression("log(2,3)"), " 2 3  log ")
        self.assertRaises(custom_exc.VerifyError, expproc.verify_expression, "((1+2)")
        self.assertRaises(custom_exc.VerifyError, expproc.verify_expression, "pow(2,,3)")
        self.assertRaises(custom_exc.VerifyError, expproc.verify_expression, "(1+2)p")
        self.assertRaises(custom_exc.VerifyError, expproc.verify_expression, "pow(2*(2+3, 3)")
        self.assertRaises(custom_exc.VerifyError, expproc.verify_expression, "(1+2))")

    def test_calculate_expression(self):
        self.assertEqual(calcexp.calculate_expression("1 2 +"), 3)
        self.assertEqual(calcexp.calculate_expression("1.5 2.5 +"), 4.0)
        self.assertAlmostEqual(calcexp.calculate_expression("pi e +"), 5.859874482048838)
        self.assertAlmostEqual(calcexp.calculate_expression("pi sin"), 0.0)
        self.assertRaises(custom_exc.VerifyError, calcexp.calculate_expression, "1 + *")
        self.assertRaises(custom_exc.VerifyError, calcexp.calculate_expression, "1 sin log")
        self.assertRaises(custom_exc.VerifyError, calcexp.calculate_expression, "1 2 + 3 * 4")
        self.assertRaises(ValueError, calcexp.calculate_expression, "2 neg 0.5 ^")
        self.assertRaises(ZeroDivisionError, calcexp.calculate_expression, "1 0 /")
