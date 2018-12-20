import unittest
import math
from pycalc.pycalc import (
    find_right_element,
    find_left_element,
    replace_long_unaries,
    checking_and_solving_comparison,
    calc_by_position_of_sign,
    calc_string,
    find_and_replace_consts,
    add_implicit_mult,
    solve_brackets,
    solve_functions,
    replace_spaces,
    calc,
    MissingArgumentException,
    BracketsNotBalancedException,
    UnknownFunctionException,
    UnknownElementException,
    UnexpectedSpaceExeption,
    FunctionArgumentsException,
    EmptyBracketsException
)


class TestPycalc(unittest.TestCase):

    def test_find_left_number_near_the_sign(self):
        self.assertEqual(find_left_element("2+2", 1), ["2", 0])

    def test_find_left_neg_number_near_the_sign_test(self):
        self.assertEqual(find_left_element("4*-3+3", 4), ["-3", 2])

    def test_find_right_number_near_the_sign(self):
        self.assertEqual(find_right_element("2+2", 1), ["2", 2])

    def test_find_right_neg_number_near_the_sign(self):
        self.assertEqual(find_right_element("2*2+3*-4", 5), ["-4", 7])

    def test_replaces_long_unaries_before_number(self):
        self.assertEqual(replace_long_unaries("---+-+-3"), "-3")

    def test_replaces_long_unaries_in_middle_of_expression(self):
        self.assertEqual(replace_long_unaries("3--+-+--+-4"), "3+4")

    def test_replaces_long_unaries_in_the_end_of_expression(self):
        with self.assertRaises(MissingArgumentException):
            replace_long_unaries("3--+-+--+-")

    def test_find_and_replace_consts_with_e_const(self):
        self.assertEqual(find_and_replace_consts("e"), str(math.e))

    def test_find_and_replace_consts_in_expression(self):
        result = "1+4*"+str(math.e)+"+"+str(math.pi)
        self.assertEqual(find_and_replace_consts("1+4*e+pi"), result)

    def test_find_and_replace_consts_with_no_consts(self):
        self.assertEqual(find_and_replace_consts("e"), str(math.e))

    def test_checking_and_solving_comparison_on_comparison_without_solving(self):
        self.assertEqual(checking_and_solving_comparison("3<2"), [False, True])

    def test_checking_and_solving_comparison_on_comparison_with_solving(self):
        self.assertEqual(checking_and_solving_comparison("3+5<2+10"), [True, True])

    def test_checking_and_solving_comparison_on_expression_without_comparison(self):
        self.assertEqual(checking_and_solving_comparison("3+5"), ["3+5", False])

    def test_calc_by_position_of_sign(self):
        self.assertEqual(calc_by_position_of_sign(5, "3+4+5*7"), [35.0, 4, 6])

    def test_calc_by_position_of_sign_with_neg_left_number(self):
        self.assertEqual(calc_by_position_of_sign(2, "-5*7"), [(float)(-5*7), 0, 3])

    def test_calc_by_position_of_sign_with_zero_pointer(self):
        with self.assertRaises(MissingArgumentException):
            calc_by_position_of_sign(0, "-5*7")

    def test_calc_by_position_of_sign_with_no_right_arg_because_of_end_of_expr(self):
        with self.assertRaises(MissingArgumentException):
            calc_by_position_of_sign(1, "7*")

    def test_calc_by_position_of_sign_with_no_right_arg(self):
        with self.assertRaises(MissingArgumentException):
            calc_by_position_of_sign(1, "7*/3")

    def test_calc_string_with_unaries(self):
        self.assertEqual(calc_string("-5*7"), (float)(-5*7))

    def test_calc_string_with_three_signs(self):
        self.assertEqual(calc_string("-5*7*4^2"), (float)(-5*7*4**2))

    def test_calc_string_check_associative(self):
        self.assertEqual(calc_string("2+2*2"), (float)(2+2*2))

    def test_calc_string_check_associative_on_powers(self):
        self.assertEqual(calc_string("2^2^2"), (float)(2**2**2))

    def test_add_implicit_multiplication_sign_after_brackets(self):
        self.assertEqual(add_implicit_mult("(3+4)2"), "(3+4)*2")

    def test_add_implicit_multiplication_sign_before_brackets(self):
        self.assertEqual(add_implicit_mult("2(3+4)"), "2*(3+4)")

    def test_add_implicit_multiplication_sign_between_brackets(self):
        self.assertEqual(add_implicit_mult("(3+4)(2+3)"), "(3+4)*(2+3)")

    def test_add_implicit_multiplication_sign_before_func(self):
        self.assertEqual(add_implicit_mult("3sin(3)"), "3*sin(3)")

    def test_add_implicit_multiplication_sign_before_const(self):
        self.assertEqual(add_implicit_mult("3e"), "3*e")

    def test_add_implicit_multiplication_sign_after_func(self):
        self.assertEqual(add_implicit_mult("sin(3)3"), "sin(3)*3")

    def test_add_implicit_multiplication_sign_after_const(self):
        self.assertEqual(add_implicit_mult("e3"), "e*3")

    def test_add_implicit_multiplication_sign_between_consts(self):
        self.assertEqual(add_implicit_mult("pie"), "pi*e")

    def test_solve_brackets_general(self):
        self.assertEqual(solve_brackets("(2+3)*3"), "5.0000000000000000*3")

    def test_solve_brackets_with_unbalanced_brackets(self):
        with self.assertRaises(BracketsNotBalancedException):
            solve_brackets("2+3(")

    def test_solve_brackets_with_empty_brackets(self):
        with self.assertRaises(EmptyBracketsException):
            solve_brackets("2+3()")

    def test_solve_functions_general(self):
        self.assertEqual(solve_functions("sin(3)"), str(math.sin(3)))

    def test_solve_functions_with_two_elems(self):
        self.assertEqual(solve_functions("sin(3)+cos(3)"), str(math.sin(3))+'+'+str(math.cos(3)))

    def test_solve_functions_with_two_args(self):
        self.assertEqual(solve_functions("log(120,10)"), str(math.log(120, 10)))

    def test_solve_functions_with_solving_in_args(self):
        self.assertEqual(solve_functions("sin(3+5)"), str(math.sin(3+5)))

    def test_solve_functions_with_wrong_number_of_arguments(self):
        with self.assertRaises(FunctionArgumentsException):
            solve_functions("log(3,4,5)")

    def test_solve_functions_with_wrong_function_name(self):
        with self.assertRaises(UnknownFunctionException):
            solve_functions("logs(3)")

    def test_solve_functions_with_wrong_element_name(self):
        with self.assertRaises(UnknownElementException):
            solve_functions("3+logs+3")

    def test_replace_spaces_in_func(self):
        self.assertEqual(replace_spaces("sin(3 + 5)"), "sin(3+5)")

    def test_replace_spaces_in_func_with_two_args(self):
        self.assertEqual(replace_spaces("log(10, 5)"), "log(10,5)")

    def test_replace_spaces_err_in_comparison_sign(self):
        with self.assertRaises(UnexpectedSpaceExeption):
            replace_spaces("3< =4")

    def test_replace_spaces_err_func(self):
        with self.assertRaises(UnexpectedSpaceExeption):
            replace_spaces("sin (3+4)")

    def test_replace_spaces_for_implicit_mult_number_before_func(self):
        self.assertEqual(replace_spaces("2 sin(3)"), "2sin(3)")

    def test_replace_spaces_for_implicit_mult_number_after_func(self):
        self.assertEqual(replace_spaces("sin(3) 2"), "sin(3)2")

    def test_replace_spaces_for_implicit_mult_between_brackets(self):
        self.assertEqual(replace_spaces("(2+3) (3+4)"), "(2+3)(3+4)")

    def test_replace_spaces_for_implicit_mult_with_const_after_number(self):
        self.assertEqual(replace_spaces("2 e"), "2e")

    def test_replace_spaces_for_implicit_mult_with_const_before_number(self):
        self.assertEqual(replace_spaces("pi 2"), "pi2")

    def test_calc_general(self):
        self.assertEqual(calc("3+log(e)+4/2^2"), 3+math.log(math.e)+4/2**2)

    def test_calc_with_unaries(self):
        self.assertEqual(calc("3+log(e)+--+-4/2^2"), 3+math.log(math.e)+--+-4/2**2)


if __name__ == "__main__":
    unittest.main()
