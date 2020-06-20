//
// Created by bill on 6/20/20.
//
#include <iostream>

using namespace std;

int main() {
    int num_cases, n;
    cin >> num_cases;
    for (int i = 0; i < num_cases; i++) {
        cin >> n;
        if (n == 1) {
            cout << 1 << endl;
        } else if (n % 2 == 0) {
            cout << n / 2 << endl;
        } else {
            cout << (n - 1) / 2 << endl;
        }
    }
}
