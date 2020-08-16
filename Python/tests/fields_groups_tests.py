from ..fields_groups import *
import unittest

class FieldsGroupsTests(unittest.TestCase):

    # ----------Polynomial modulo tests----------
    def test_polynomial_modulo_remainder0(self):
        # Remainder 0 case:
        # https://www.symbolab.com/solver/polynomial-long-division-calculator/long%20division%20%5Cfrac%7B1%20%2B%20x%5E%7B2%7D%20%2B%20x%5E%7B4%7D%20%2B%20x%5E%7B5%7D%20%2B%20x%5E%7B6%7D%20%2B%20x%5E%7B7%7D%7D%7B1%20%2B%20x%20%2B%20x%5E%7B2%7D%7D
        f = [1, 0, 1, 0, 1, 1, 1, 1]  # 1 + x^2 + x^4 + x^5 + x^6 + x^7
        g = [1, 1, 1, 0, 0, 0, 0, 0]  # 1 + x + x^2
        self.assertTrue(all(i == 0 for i in polynomial_modulo(f, g)))

    def test_polynomial_modulo_remainder1(self):
        # Should return 1:
        # https://www.symbolab.com/solver/polynomial-long-division-calculator/long%20division%20%5Cfrac%7B1%20%2B%20x%5E%7B2%7D%20%2B%20x%5E%7B3%7D%20%2B%20x%5E%7B5%7D%20%2B%20x%5E%7B6%7D%7D%7B1%20%2B%20x%7D
        f = [1, 0, 1, 1, 0, 1, 1, 0]  # 1 + x^2 + x^3 + x^5 + x^6
        g = [1, 1, 0, 0, 0, 0, 0, 0]  # 1 + x
        result = polynomial_modulo(f, g)
        self.assertTrue(result[0] == 1)
        self.assertTrue(all(i == 0 for i in result[1:]))

    def test_polynomial_modulo_remainder_poly(self):
        # Should return x^2 + 1:
        # https://www.symbolab.com/solver/polynomial-long-division-calculator/long%20division%20%5Cfrac%7B1%20%2B%20x%20%2B%20x%5E%7B2%7D%20%2B%20x%5E%7B4%7D%20%2B%20x%5E%7B7%7D%7D%7B1%20%2B%20x%5E%7B3%7D%20%2B%20x%5E%7B6%7D%7D
        f = [1, 1, 1, 0, 1, 0, 0, 1]  # 1 + x + x^2 + x^4 + x^7
        g = [1, 0, 0, 1, 0, 0, 1, 0]  # 1 + x^3 + x^6
        result = polynomial_modulo(f, g)
        expected = [1, 0, 1, 0, 0, 0, 0, 0]
        self.assertEqual(expected, result)

    def test_polynomial_modulo_remainder_f_x(self):
        # Should return f(x):
        f = [1, 0, 1, 1, 0, 1, 1, 0]  # 1 + x^2 + x^3 + x^5 + x^6
        g = [1, 1, 0, 0, 0, 0, 0, 1]  # 1 + x + x^7
        self.assertEqual(f, polynomial_modulo(f, g))

    # ----------Multiplicative Inverse tests/results----------
    def test_mult_inverse_random(self):
        # Random test, confirmed via: http://wims.unice.fr/wims/wims.cgi?module=tool/algebra/calcff.en
        # Should return x^6 + x^5
        m = [1, 1, 0, 1, 1, 0, 0, 0, 1]  # x^8 + x^4 + x^3 + x + 1
        a = [0, 1, 1, 0, 1, 0, 0, 0, 0]  # x + x^2 + x^4
        result = multiplicative_inverse_galois_field(a, m)
        expected = [0, 0, 0, 0, 0, 1, 1, 0, 0]
        self.assertEqual(expected, result)

    def test_mult_inverse_pset(self):
        # PSET Q1a.1:
        # Should return x^6 + x^5 + x^4 + x^2 + x + 1, confirmed via above site/calculator
        m = [1, 1, 0, 1, 1, 0, 0, 0, 1]  # x^8 + x^4 + x^3 + x + 1
        a = [0, 0, 1, 1, 1, 1, 0, 0, 0]  # x^5 + x^4 + x^3 + x^2
        result = multiplicative_inverse_galois_field(a, m)
        expected = [1, 1, 1, 0, 1, 1, 1, 0, 0]
        self.assertEqual(expected, result)

    # ----------Discrete log tests/results ----------
    def test_discrete_log_simple(self):
        # Simple test, should return 3:
        generator = [1, 1, 0, 0, 0, 0, 0, 0, 0]  # 1 + x
        m = [1, 0, 1, 1, 0, 0, 0, 0, 0]  # 1 + x^2 + x^3
        gPowX = [0, 1, 0, 0, 0, 0, 0, 0, 0]  # x
        self.assertEqual(3, discrete_log(gPowX, generator, m))

    def test_discrete_log_medium(self):
        # Medium test, should return 7
        generator = [1, 1, 0, 0, 0, 0, 0, 0, 0]  # 1 + x
        m = [1, 1, 0, 0, 1, 0, 0, 0, 0]  # 1 + x + x^4
        gPowX = [1, 0, 1, 1, 0, 0, 0, 0, 0]  # 1 + x^2 + x^3
        self.assertEqual(7, discrete_log(gPowX, generator, m))

    def test_discrete_log_pset(self):
        # PSET Q1a.2:
        generator = [1, 1, 1, 0, 1, 0, 0, 0, 0]  # 1 + x + x^2 + x^4
        m = [1, 1, 0, 1, 1, 0, 0, 0, 1]  # 1 + x + x^3 + x^4 + x^8
        gPowX = [0, 0, 1, 0, 0, 0, 1, 1, 0]  # x^2 + x^6 + x^7
        self.assertEqual(233, discrete_log(gPowX, generator, m))
