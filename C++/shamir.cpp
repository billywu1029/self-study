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
    assert(n >= t);
    vector<pair<int, int>> shares;
    vector<int> p_x = construct_polynomial(t-1, s);
    random_device rd;  // Used to obtain a seed for the mersenne twister rng
    mt19937 rng(rd());  // Standard mersenne_twister_engine seeded with rd()

    shuffle(p_x.begin(), p_x.end(), rng);
    shares.reserve(n);
    for (int x = 1; x <= n; x++) {
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

// Evaluate polynomial
// Evaluate P(x) for some value x, P(x) assumed to be at least 2nd degree
int evaluate_polynomial(const vector<int> &p_x, int x) {
    int result = 0;  // TODO: Potentially need to ensure no integer overflows
    size_t n = p_x.size();
    assert(n >= 2);

    result += p_x[n - 1];
    for (size_t i = n - 1; i > 0; i--) {
        result += p_x[i - 1] * x;
        x *= x;
    }
    return result;
}

int main(int argc, char** argv) {
    assert (argc == 4);
    int n, t, s;
    n = atoi(argv[1]);
    t = atoi(argv[2]);
    s = atoi(argv[3]);
    cout << "n shares: " << n << endl;
    cout << "t threshold shares: " << t << endl;
    cout << "s secret: " << s << endl;  // TODO: this defeats the purpose of the secret hehe
    vector<pair<int, int>> shares = generate_shares(n, t, s);
    for (int i = 0; i < shares.size(); i++) {
        cout << "share " << i << ": (" << shares[i].first << ", " << shares[i].second << ")\n";
    }
    return 0;
}

