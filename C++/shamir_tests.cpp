//
// Created by bill on 7/23/20.
//
#include "shamir.cpp"
#include <gtest/gtest.h>

/* Testing Partitions:
 * construct_polynomial(const uint64_t degree, const uint64_t secret):
 *  - TODO: Add a seed parameter and figure out how to set the seed of the rng in the function to test reliably
 *  - seed = 0, > 0
 *  - degree = 0, 1, > 1
 *  - secret = 0, > 0
 * evaluate_polynomial(const vector<uint64_t> &p_x, const uint64_t x):
 *  - x = 0, > 0
 *  - p_x second order, > 2nd order, same/different coefficients, 0, >0 coefficients set to 0
 * generate_shares(const uint64_t n, const uint64_t t, const uint64_t s):
 *  - n = t, n > t
 *  - t = 1, > 1
 *  - s = 0, > 0
 * lagrange_interpolate(const vector<pair<uint64_t, uint64_t>> &points, const uint64_t k):
 *  - k = 1, > 1
 *  - points correspond to linear, quadratic, order > 2 polynomials
 *  - points.size() == k, > k
 */

TEST(ShamirTest, ExampleName) {
    // Do stuff
    int result = 1;
    int answer = 2;
    EXPECT_EQ(result, answer);

}

//int main() {
//    RUN_ALL_TESTS();
//}
