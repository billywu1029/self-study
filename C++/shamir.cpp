//
// Created by bill on 7/21/20.
// Implements Shamir's Secret Sharing scheme.
// Polynomials will be organized such that p_x[0] is the n-1th degree coefficient, and p_x[-1] is the constant term
// Also operates in a finite field characterized by 2^32 - 5 (largest 32 bit prime), for 32-bit security.
//

#include <iostream>
#include <cassert>
#include <vector>
#include <utility>  // std::pair
#include <random>  // std::random_device, std::mt19937 (mersenne twister engine), std::uniform_int_distribution
#include <algorithm>  // std::shuffle (for permutation of indices)
#include <cstdint>  // uint64_t

using namespace std;

// Smallest prime < 2^32, this must be prime otherwise inv = x^(p-2) mod p wouldn't hold (Fermat's Little Theorem)
uint64_t PRIME_FF = (1ULL << 32) - 5;

vector<uint64_t> construct_polynomial(uint64_t degree, uint64_t s);
uint64_t evaluate_polynomial(const vector<uint64_t> &p_x, uint64_t x);

// TODO: Abstract all of these away to a finite field arithmetic handler, and create operator overloads for these
inline uint64_t add_ff(const uint64_t x, const uint64_t y, const uint64_t p = PRIME_FF) {
    return (x + y) % p;
}

inline uint64_t subtract_ff(const uint64_t x, const uint64_t y, const uint64_t p = PRIME_FF) {
    return y > x ? add_ff(x, p-y) : (x - y);
}

inline uint64_t multiply_ff(const uint64_t x, const uint64_t y, const uint64_t p = PRIME_FF) {
    return (x * y) % p;
}

uint64_t pow_ff(uint64_t base, uint64_t exp, const uint64_t p = PRIME_FF) {
    // Borrowed from: https://stackoverflow.com/questions/8496182/calculating-powa-b-mod-n
    base %= p;
    uint64_t result = 1;
    while (exp > 0) {
        if (exp & 1) result = multiply_ff(result, base, p);
        base = multiply_ff(base, base, p);
        exp >>= 1;
    }
    return result;
}

// Finds the multiplicative inverse of x within the field characterized by p
uint64_t multiplicative_inverse(const uint64_t x, const uint64_t p = PRIME_FF) {
    // Don't need Euclid's Extended GCD algorithm since our field is characterized by p, which is prime
    return pow_ff(x, p - 2);
}

uint64_t divide_ff(const uint64_t x, const uint64_t y, const uint64_t p = PRIME_FF) {
    return multiply_ff(x, multiplicative_inverse(y, p));
}

// Share generation
// Accept input n: num shares, t: threshold num shares (to decrypt), s: secret
vector<pair<uint64_t, uint64_t>> generate_shares(const uint64_t n, const uint64_t t, const uint64_t s) {
    assert(n >= t);
    vector<pair<uint64_t, uint64_t>> shares;
    vector<uint64_t> p_x = construct_polynomial(t-1, s);
    shares.reserve(n);
    for (uint64_t x = 1; x <= n; x++) {
        pair<uint64_t, uint64_t> share;
        share = make_pair(x, evaluate_polynomial(p_x, x));
        shares.push_back(share);
    }
    // [DEBUG]
    for (uint64_t exp = t; exp > 1; exp--) {
        cout << p_x[t - exp] << "x^" << exp - 1 << " + ";
    }
    cout << s << " = 0" << endl;

    return shares;
}

// Construct polynomial
// P(x) of degree t-1. Random coefficients, constant term is the secret s, eg 2x^3 + x^2 + 10x + 420
vector<uint64_t> construct_polynomial(const uint64_t degree, const uint64_t s) {
    vector<uint64_t> p_x;
    random_device rd;
    mt19937_64 rng(rd());
    uniform_int_distribution<uint64_t> distrib(0, PRIME_FF);

    p_x.reserve(degree + 1);
    for (int i = 0; i < degree; i++) {
        p_x.push_back(distrib(rng));
    }
    p_x.push_back(s);
    return p_x;
}

// Evaluate polynomial
// Evaluate P(x) for some value x, P(x) assumed to be at least 2nd degree
uint64_t evaluate_polynomial(const vector<uint64_t> &p_x, const uint64_t x) {
    // Clever way to evaluate this while staying within the finite field:
    // result = a_0 + a_1*x + a_2*x^2 + ... ... mod p
    //        = a_0 + x( a_1 + x( a_2 + ... ... ) mod p ) mod p
    uint64_t result = 0;
    for (uint64_t coeff : p_x) {
        result = multiply_ff(result, x);
        result = add_ff(result, coeff);
    }
    return result;
}

// Lagrange Interpolation given k points, k >= t (the threshold), evaluated at x = 0. Assumes that points are distinct
uint64_t lagrange_interpolate(const vector<pair<uint64_t, uint64_t>> &points, const uint64_t k) {
    uint64_t result = 0;
    uint64_t prod_num = 1;
    uint64_t prod_denom = 1;
    for (size_t i = 0; i < k; i++) {
        prod_num = multiply_ff(prod_num, points[i].first);
    }

    for (size_t j = 0; j < k; j++) {
        uint64_t x_j = points[j].first;
        uint64_t prod = divide_ff(prod_num, x_j);
        for (size_t m = 0; m < k; m++) {
            if (m == j) continue;
            uint64_t denom_term = subtract_ff(points[m].first, x_j);
            prod_denom = multiply_ff(prod_denom, denom_term);
        }
        prod = divide_ff(prod, prod_denom);
        prod = multiply_ff(prod, points[j].second);
        result = add_ff(result, prod);
    }
    return result;
}

// Reconstruct Secret
// Reconstruct the secret via Lagrange Interpolation over the finite field specified by PRIME_FF
uint64_t reconstruct_secret(const vector<pair<uint64_t, uint64_t>> &shares, const uint64_t t) {
    assert(shares.size() >= t);
    return lagrange_interpolate(shares, t);
}

int main(int argc, char** argv) {
    uint64_t n, t, s;
//    assert (argc == 4);
//    n = atoi(argv[1]);
//    t = atoi(argv[2]);
//    s = atoi(argv[3]);
    n = 3;
    t = 2;
    s = 69;
    cout << "n shares: " << n << endl;
    cout << "t threshold shares: " << t << endl;
    cout << "s secret: " << s << endl;
    vector<pair<uint64_t, uint64_t>> shares = generate_shares(n, t, s);
    for (int i = 0; i < shares.size(); i++) {
        cout << "share " << i << ": (" << shares[i].first << ", " << shares[i].second << ")\n";
    }

    uint64_t secret_reconstructed = reconstruct_secret(shares, t);
    cout << secret_reconstructed << endl;

//    vector<pair<uint64_t, uint64_t>> testshares;
//    testshares.emplace_back(1, 2);
//    testshares.emplace_back(3, 0);
//
//    uint64_t test = lagrange_interpolate(testshares, 2);
//    uint64_t test2 = multiply_ff(PRIME_FF, divide_ff(3, PRIME_FF));
//    cout << test2 << endl;
    return 0;
}

