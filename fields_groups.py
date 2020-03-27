"""
Note: Refactor this eventually and make a polynomial class that has a underlying List[int] or binary bits representation
"""
DISCRETE_LOG_MAX_THRESH = 2 ** 8 + 1  # Anything beyond this means it doesn't exist
GALOIS_FIELD_ORDER = 2 ** 8
GALOIS_FIELD_P = 2
GALOIS_FIELD_N = 8

def multiplicative_inverse_galois_field(f_x: list, m_x: list):
    """Finds the multiplicative inverse of f(x) in GF(p^n) (defined by m(x)) using Fermat's Little Theorem:
    a^(p^n - 1) = 1 mod m(x) --> a^(-1) = a^(p^n - 2) mod m(x)"""
    # TODO: Repeated squaring, instead of 1 iteration at a time
    result = f_x[:]
    for _ in range(GALOIS_FIELD_ORDER - 3):  # Subtract an extra 1 since we start with f(x) already (f->f^2 == 1 iter)
        result = polynomial_mult_galois_field(result, f_x, m_x)
    return result


def discrete_log(a: list, base: list, m_x: list) -> int:
    """
    TLDR: b^k = a mod m_x, solve for k
    Calculates the discrete logarithm of a to the base b, within a Galois field GF(n), defined by the polynomial m(x)
    Returns the result as an int, representing the degree deg(m_x) polynomial of the mathematical result.
    Note that a, base, and m_x are all List[int] such as [0, 0, 1, 5, 2, 0, 0, 0] representing x^5 + 5x^4 + 2x^3
    """
    # TODO: Repeated squaring
    base_cpy = base[:]
    result = base[:]
    k = 1
    while result != a and k < DISCRETE_LOG_MAX_THRESH:
        result = polynomial_mult_galois_field(result, base_cpy, m_x)
        k += 1
    if k >= DISCRETE_LOG_MAX_THRESH:
        raise RuntimeError("sum ting wong")
    return k


def polynomial_mult_galois_field(f_x: list, g_x: list, m_x: list) -> list:
    """
    Returns the result of polynomial multiplication of f(x) * g(x) in GF(n), defined by m(x).
    Final result polynomial, f(x), and g(x) all represented as a List[int] of coefficients.
    """
    assert len(f_x) == len(g_x) == len(m_x)
    result = [i % GALOIS_FIELD_P for i in polynomial_mult(f_x, g_x)]
    result = polynomial_modulo(result, m_x)
    return [i % GALOIS_FIELD_P for i in result]


def polynomial_mult(f_x: list, g_x: list) -> list:
    # Replace with shifts + appropriate bithacks if choosing that optimization
    result = [0] * (len(f_x) + len(g_x) - 1)
    for i, ci in enumerate(f_x):
        if ci == 0:
            continue
        else:
            for j, cj in enumerate(g_x):
                result[i + j] = result[i + j] + (ci * cj)
    return result

def polynomial_modulo(f_x: list, m_x: list) -> list:
    """
    Returns the result of f(x) mod m(x), AKA the remainder after doing polynomial long division.
    Note, f(x) and m(x) must have degree >= 0
    """
    # Replace this with combination of bithack versions of poly add, poly multiply, and poly inv if doing bithacks
    result = f_x[:]  # After all iterations of long division are complete, this is the final modulo result
    nonzero_ind_mx = last_nonzero_ind(m_x)  # Last non-zero coefficient == degree(m(x))
    assert nonzero_ind_mx is not None
    nonzero_ind_result = last_nonzero_ind(result)  # Last non-zero coefficient of the result
    assert nonzero_ind_result is not None

    while nonzero_ind_result >= nonzero_ind_mx:
        # tmp and deg_diff together form the result of the jth iter of long division: cx^i, where c=tmp and i=deg_diff
        tmp = result[nonzero_ind_result] / m_x[nonzero_ind_mx]  # Quotient on top in long division for this iteration
        assert tmp == 1  # Hack check for now, need everything to be in binary for this to work
        degree_diff = nonzero_ind_result - nonzero_ind_mx

        subtraction_term = [0] * degree_diff  # First shift polynomial by x^degree_diff, pad with 0s
        subtraction_term.extend([-tmp * i for i in m_x])  # Then "extend" with m(x), so m(x) * x^degree_diff
        result = polynomial_addition_galois_field(result, subtraction_term)
        nonzero_ind_result = last_nonzero_ind(result)
        if nonzero_ind_result is None:  # mod result is 0, since result is just the 0 polynomial
            break

    # Need to truncate the unnecessary 0s at the end + verify that nothing went wrong
    assert all(i == 0 for i in result[nonzero_ind_mx:])
    return result[:len(m_x)]  # TODO: Careful here, should probably use nonzero_ind_mx


def last_nonzero_ind(f_x: list, default=None):
    # Replace this w the bithack that gets the last nonzero bit if doing bithack approach for better performance
    result = default
    for i, c in enumerate(f_x):
        if c != 0:
            result = i
    return result


def polynomial_addition_galois_field(f_x: list, g_x: list) -> list:
    # Replace this with xors if doing bithacks
    short, long = (f_x, g_x) if len(f_x) < len(g_x) else (g_x, f_x)
    result = long[:]
    for i, ci in enumerate(short):
        result[i] = (result[i] + ci) % GALOIS_FIELD_P
    return result


if __name__ == "__main__":
    bruh = [1, 0, 1, 0, 1, 1, 1, 0, 0]
    m = [1, 1, 0, 1, 1, 0, 0, 0, 1]
    print(polynomial_mult_galois_field(bruh, bruh, m))
