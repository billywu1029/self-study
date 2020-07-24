//
// Created by bill on 7/21/20.
// Implements Shamir's Secret Sharing scheme.
// Polynomials will be organized such that p_x[0] is the n-1th degree coefficient, and p_x[-1] is the constant term
// Also operates in a finite field characterized by 2^64 - 59 (largest 64 bit prime), for 64-bit security.
//

#include <iostream>
#include <cassert>
#include <vector>
#include <utility>  // std::pair
#include <random>  // std::random_device, std::mt19937 (mersenne twister engine), std::uniform_int_distribution
#include <algorithm>  // std::shuffle (for permutation of indices)
#include <cstdint>  // uint64_t

using namespace std;

// Trick to get 2^64 - 59 without pow or even bitshifting
uint64_t PRIME_FF = -59;

vector<uint64_t> construct_polynomial(uint64_t degree, uint64_t s);
uint64_t evaluate_polynomial(const vector<uint64_t> &p_x, uint64_t x);

// Share generation
// Accept input n: num shares, t: threshold num shares (to decrypt), s: secret
vector<pair<uint64_t, uint64_t>> generate_shares(const uint64_t n, const uint64_t t, const uint64_t s) {
    assert(n >= t);
    vector<pair<uint64_t, uint64_t>> shares;
    vector<uint64_t> p_x = construct_polynomial(t-1, s);
    random_device rd;  // Used to obtain a seed for the mersenne twister rng
    mt19937_64 rng(rd());  // Standard mersenne_twister_engine (64-bits) seeded with rd()

    shuffle(p_x.begin(), p_x.end(), rng);
    shares.reserve(n);
    for (uint64_t x = 1; x <= n; x++) {
        pair<uint64_t, uint64_t> share;
        share = make_pair(x, evaluate_polynomial(p_x, x));
        shares.push_back(share);
    }
    return shares;
}

// Construct polynomial
// P(x) of degree t-1. Random coefficients, constant term is the secret s
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
    // TODO: How is overflow handled? Perhaps should reduce _PRIME_FF to avoid some janky math that could cause bugs..?
    uint64_t result = 0;
    for (size_t i = p_x.size(); i > 0; i--) {
        result += p_x[i-1];
        result *= x;
        result %= PRIME_FF;
    }
    return result;
}

int main(int argc, char** argv) {
    assert (argc == 4);
    uint64_t n, t, s;
    n = atoi(argv[1]);
    t = atoi(argv[2]);
    s = atoi(argv[3]);
    cout << "n shares: " << n << endl;
    cout << "t threshold shares: " << t << endl;
    cout << "s secret: " << s << endl;  // TODO: this defeats the purpose of the secret hehe
    vector<pair<uint64_t, uint64_t>> shares = generate_shares(n, t, s);
    for (int i = 0; i < shares.size(); i++) {
        cout << "share " << i << ": (" << shares[i].first << ", " << shares[i].second << ")\n";
    }
    return 0;
}

