import unittest

from toolkit.calculator import calculate
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    InvalidValueError,
    MissingOperandError,
    TwoBinaryOperatorsError,
    UnbalancedParenthesesError,
)


class TestCalculator(unittest.TestCase):
    def test_1(self):
        self.assertEqual(calculate("4+7"), 11.0)

    def test_subtract(self):
        self.assertEqual(calculate("10-5"), 5.0)

    def test_multiply(self):
        self.assertEqual(calculate("3*7"), 21.0)

    def test_divide(self):
        self.assertEqual(calculate("10/4"), 2.5)

    def test_priority(self):
        self.assertEqual(calculate("2+3*4"), 14.0)

    def test_left_associativity(self):
        self.assertEqual(calculate("10-3-2"), 5.0)

    def test_spaces(self):
        self.assertEqual(calculate("  3   +   4  "), 7.0)

    def test_float_numbers(self):
        self.assertAlmostEqual(calculate("0.1+0.2"), 0.3)

    def test_unary_minus(self):
        self.assertEqual(calculate("-5"), -5.0)

    def test_unary_plus(self):
        self.assertEqual(calculate("+5"), 5.0)

    def test_unary_after_operator(self):
        self.assertEqual(calculate("3*-2"), -6.0)

    def test_binary_and_unary_minus(self):
        self.assertEqual(calculate("2--3"), 5.0)

    def test_parentheses(self):
        self.assertEqual(calculate("(1+2)*3"), 9.0)

    def test_nested_parentheses(self):
        self.assertEqual(calculate("((2))"), 2.0)

    def test_unary_before_parentheses(self):
        self.assertEqual(calculate("3*-(1+1)"), -6.0)

    def test_result_is_float(self):
        self.assertIsInstance(calculate("2+2"), float)

    def test_empty_expression(self):
        with self.assertRaises(EmptyExpressionError):
            calculate("")

    def test_only_spaces(self):
        with self.assertRaises(EmptyExpressionError):
            calculate("   ")

    def test_invalid_character(self):
        with self.assertRaises(InvalidCharacterError):
            calculate("3 $ 4")

    def test_invalid_number(self):
        with self.assertRaises(InvalidValueError):
            calculate("1.2.3")

    def test_missing_operand_end(self):
        with self.assertRaises(MissingOperandError):
            calculate("3 +")

    def test_missing_operand_start(self):
        with self.assertRaises(MissingOperandError):
            calculate("*2")

    def test_two_numbers_in_a_row(self):
        with self.assertRaises(MissingOperandError):
            calculate("3 4")

    def test_two_binary_operators(self):
        with self.assertRaises(TwoBinaryOperatorsError):
            calculate("3 * / 2")

    def test_division_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            calculate("5/0")

    def test_division_by_zero_in_parentheses(self):
        with self.assertRaises(DivisionByZeroError):
            calculate("10/(5-5)")

    def test_unclosed_parenthesis(self):
        with self.assertRaises(UnbalancedParenthesesError):
            calculate("(3+4")

    def test_extra_closing_parenthesis(self):
        with self.assertRaises(UnbalancedParenthesesError):
            calculate("3+4)")

    def test_empty_parentheses(self):
        with self.assertRaises(MissingOperandError):
            calculate("()")


class TestCalculatorComplex(unittest.TestCase):
    def test_long_sum(self):
        self.assertEqual(calculate("1+2+3+4+5+6+7+8+9+10"), 55.0)

    def test_long_subtraction(self):
        self.assertEqual(calculate("100-10-20-30-40"), 0.0)

    def test_long_multiplication(self):
        self.assertEqual(calculate("2*3*4*5"), 120.0)

    def test_long_division(self):
        self.assertEqual(calculate("1000/10/5/2"), 10.0)

    def test_all_operators(self):
        self.assertEqual(calculate("2+3*4-5/5+6*2-1"), 24.0)

    def test_long_mixed(self):
        self.assertEqual(calculate("1+2*3-4/2+5*6-7+8/4*3"), 34.0)

    def test_mul_div_left_to_right(self):
        self.assertEqual(calculate("100/10*5"), 50.0)

    def test_negative_result(self):
        self.assertEqual(calculate("3-10*2"), -17.0)

    def test_many_floats(self):
        self.assertAlmostEqual(calculate("0.1+0.2+0.3+0.4"), 1.0)

    def test_floats_with_priority(self):
        self.assertAlmostEqual(calculate("1.5*2+0.25*4"), 4.0)

    def test_two_groups(self):
        self.assertEqual(calculate("(1+2)*(3+4)"), 21.0)

    def test_difference_of_groups(self):
        self.assertEqual(calculate("((1+2)*(3+4))-((5-3)*(2+1))"), 15.0)

    def test_deep_nesting(self):
        self.assertEqual(calculate("2*(3+(4*(5-2)))"), 30.0)

    def test_deep_nesting_2(self):
        self.assertEqual(calculate("((((((2+3)*2)-4)/3)+1)*5)"), 15.0)

    def test_many_redundant_parentheses(self):
        self.assertEqual(calculate("(((((1)))))"), 1.0)

    def test_parentheses_change_priority(self):
        self.assertEqual(calculate("100/(10*5)"), 2.0)

    def test_subtraction_of_groups(self):
        self.assertEqual(calculate("10-(2+3)-(4-1)"), 2.0)

    def test_division_by_groups(self):
        self.assertEqual(calculate("100/(2+3)/(1+1)"), 10.0)

    def test_nested_with_priority(self):
        self.assertEqual(calculate("2+3*(4+5*(6-1))"), 89.0)

    def test_group_in_numerator_and_denominator(self):
        self.assertEqual(calculate("((2+3)*(4-1)-5)/(2+3)"), 2.0)

    def test_floats_in_parentheses(self):
        self.assertAlmostEqual(calculate("(1.5+2.5)*(3.5-1.5)/2"), 4.0)

    def test_product_of_groups_with_number(self):
        self.assertEqual(calculate("2*(3+4)*(5-1)/(1+1)"), 28.0)

    def test_negative_groups(self):
        self.assertEqual(calculate("(3-10)*(2-5)"), 21.0)

    def test_zero_group(self):
        self.assertEqual(calculate("5*(3-3)"), 0.0)

    def test_triple_unary_minus(self):
        self.assertEqual(calculate("-(-(-(3)))"), -3.0)

    def test_unary_minus_before_two_groups(self):
        self.assertEqual(calculate("-(2+3)*-(1+1)"), 10.0)

    def test_unary_chain_with_multiplication(self):
        self.assertEqual(calculate("2*-3*-4"), 24.0)

    def test_unary_plus_before_parentheses(self):
        self.assertEqual(calculate("3*+(2+1)"), 9.0)

    def test_plus_and_unary_plus(self):
        self.assertEqual(calculate("1++2"), 3.0)

    def test_plus_and_unary_minus(self):
        self.assertEqual(calculate("1+-2"), -1.0)

    def test_minus_and_unary_plus(self):
        self.assertEqual(calculate("1-+2"), -1.0)

    def test_unary_in_parentheses(self):
        self.assertEqual(calculate("2*(-3)"), -6.0)

    def test_spaces_with_parentheses(self):
        self.assertEqual(calculate(" ( 1 + 2 ) * ( 3 + 4 ) "), 21.0)

    def test_tabs_and_newlines_with_parentheses(self):
        self.assertEqual(calculate("\t(1+\n2)*3"), 9.0)

    def test_division_by_zero_expression(self):
        with self.assertRaises(DivisionByZeroError):
            calculate("1/(2-1-1)")

    def test_division_by_zero_product(self):
        with self.assertRaises(DivisionByZeroError):
            calculate("10/(4*(2-2))")

    def test_division_by_zero_in_the_middle(self):
        with self.assertRaises(DivisionByZeroError):
            calculate("10/(5-5)+1")

    def test_unclosed_nested(self):
        with self.assertRaises(UnbalancedParenthesesError):
            calculate("((1+2)*3")

    def test_extra_closing_nested(self):
        with self.assertRaises(UnbalancedParenthesesError):
            calculate("(1+2))*3")

    def test_unclosed_deep(self):
        with self.assertRaises(UnbalancedParenthesesError):
            calculate("3*(4+(5-2)")

    def test_group_after_group(self):
        with self.assertRaises(MissingOperandError):
            calculate("(1+2)(3+4)")

    def test_number_before_parenthesis(self):
        with self.assertRaises(MissingOperandError):
            calculate("2(3)")

    def test_number_after_parenthesis(self):
        with self.assertRaises(MissingOperandError):
            calculate("(1+2) 3")

    def test_two_numbers_inside_parentheses(self):
        with self.assertRaises(MissingOperandError):
            calculate("(1 2)")

    def test_operator_before_closing(self):
        with self.assertRaises(MissingOperandError):
            calculate("(1+)")

    def test_operator_before_closing_nested(self):
        with self.assertRaises(MissingOperandError):
            calculate("((1+2)*(3+))")

    def test_operator_at_start_of_group(self):
        with self.assertRaises(MissingOperandError):
            calculate("(*2)")

    def test_reversed_parentheses(self):
        with self.assertRaises(MissingOperandError):
            calculate(")(")

    def test_expression_ends_with_operator(self):
        with self.assertRaises(MissingOperandError):
            calculate("1+2*3-")

    def test_binary_operators_after_group(self):
        with self.assertRaises(TwoBinaryOperatorsError):
            calculate("(1+2)*/3")

    def test_three_signs_in_a_row(self):
        with self.assertRaises(TwoBinaryOperatorsError):
            calculate("1+++2")

    def test_double_unary_minus(self):
        with self.assertRaises(TwoBinaryOperatorsError):
            calculate("--5")

    def test_invalid_character_after_group(self):
        with self.assertRaises(InvalidCharacterError):
            calculate("((1+2)*3)$")

    def test_invalid_number_in_long_expression(self):
        with self.assertRaises(InvalidValueError):
            calculate("1.2.3+4")


if __name__ == "__main__":
    unittest.main()
