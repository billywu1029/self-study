//
// Created by bill on 7/21/20.
// Implements Shamir's Secret Sharing scheme.
// Polynomials will be organized such that p_x[0] is the n-1th degree coefficient, and p_x[-1] is the constant term
//

#include <iostream>
#include <cassert>
#include <vector>
#include <utility>  // std::pair
#include <random>  // std::random_device, std::mt19937 (mersenne twister engine), std::uniform_int_distribution
#include <algorithm>  // std::shuffle (for permutation of indices)

using namespace std;

int COEFF_MAX_VAL = 1000;

vector<int> construct_polynomial(int degree, int s);
int evaluate_polynomial(const vector<int> &p_x, int x);

// Share generation
// Accept input n: num shares, t: threshold num shares (to decrypt), s: secret
vector<pair<int, int>> generate_shares(const int n, const int t, const int s) {
    vector<pair<int, int>> shares;
    vector<int> p_x = construct_polynomial(t-1, s);
    random_device rd;  // Used to obtain a seed for the mersenne twister rng
    mt19937 rng(rd());  // Standard mersenne_twister_engine seeded with rd()

    shuffle(p_x.begin(), p_x.end(), rng);
    shares.reserve(n);
    for (int x = 0; x < n; x++) {
        pair<int, int> share;
        share = make_pair(x, evaluate_polynomial(p_x, x));
        shares.push_back(share);
    }

    return shares;
}

// Construct polynomial
// P(x) of degree t-1. Random coefficients, constant term is the secret s
vector<int> construct_polynomial(const int degree, const int s) {
    vector<int> p_x;
    random_device rd;
    mt19937 rng(rd());
    uniform_int_distribution<> distrib(0, COEFF_MAX_VAL);

    p_x.reserve(degree + 1);
    for (int i = 0; i < degree; i++) {
        p_x.push_back(distrib(rng));
    }
    p_x.push_back(s);
    return p_x;
}

int pow_int(int x, int p) {
    // Borrowed from https://stackoverflow.com/questions/1505675/power-of-an-integer-in-c
    // TODO: Consider making this iterative instead of recursive to avoid stack overflow
    if (p == 0) return 1;
    if (p == 1) return x;

    int tmp = pow_int(x, p / 2);
    if (p % 2 == 0) return tmp * tmp;
    else return x * tmp * tmp;
}

// Evaluate polynomial
// Evaluate P(x) for some value x
int evaluate_polynomial(const vector<int> &p_x, const int x) {
    int result = 0;  // TODO: Potentially need to ensure no integer overflows
    size_t n = p_x.size() - 1;  // degree of the polynomial (exponent of the highest order term)
    int x_term_pow = pow_int(x, n);
    for (size_t i = n; i >= 0; i--) {
        result += p_x[i] * x_term_pow;
        x_term_pow /= x;
    }
    return result;
}

int main(int argc, char** argv) {
    assert (argc >= 2);
    cout << argv[1] << endl;
    return 0;
}

