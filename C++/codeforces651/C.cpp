//
// Created by bill on 6/20/20.
//
#include <iostream>
#include <string>
#include <cmath>

using namespace std;

const string PLAYER1 = "Ashishgup";
const string PLAYER2 = "FastestFinger";

bool isPowerOf2(int n) {
    return (n & (n - 1)) == 0;
}

bool isPrime(int n) {
    // Assumes input n is > 2
    if (n % 2 == 0) {
        return false;
    } else {
        for (int i = 3; i < ((int) sqrt((double) n)) + 1; i += 2) {
            if (n % i == 0) {
                return false;
            }
        }
    }
    return true;
}

int main() {
    int t, n;
    cin >> t;
    for (int i = 0; i < t; i++) {
        cin >> n;
        if (n == 1) {
            cout << PLAYER2 << endl;
            continue;
        } else if (n == 2) {
            cout << PLAYER1 << endl;
            continue;
        } else if (n % 2 != 0) {
            cout << PLAYER1 << endl;
            continue;
        } else if (isPowerOf2(n)) {
            cout << PLAYER2 << endl;
            continue;
        } else {
            // Even number, not power of 2
            if (n % 4 == 0) {
                // Player 1 wins since they just divide by the product of the odd divisors and leaves 4, which wins
                cout << PLAYER1 << endl;
                continue;
            } else {
                // If n / 2 is prime, not a power of 2, and >= 3, then p1 can't ever win
                // If n / prime divisor, then left with 2, which loses
                // If n - 1, then left with an odd number, which loses
                cout << (isPrime(n / 2) ? PLAYER2 : PLAYER1) << endl;
            }
        }
    }
}
