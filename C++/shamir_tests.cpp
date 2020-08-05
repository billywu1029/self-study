//
// Created by bill on 7/23/20.
//
#include "shamir.cpp"
#include <gtest/gtest.h>

/* Testing Partitions:
 * generate_shares(const uint64_t n, const uint64_t t, const uint64_t s):
 *  -
 * construct_polynomial(const uint64_t degree, const uint64_t secret):
 *  -
 * evaluate_polynomial(const vector<uint64_t> &p_x, const uint64_t x):
 *  -
 * lagrange_interpolate(const vector<pair<uint64_t, uint64_t>> &points, const uint64_t k):
 *  -
 *
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
