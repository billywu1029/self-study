//
// Created by bill on 6/20/20.
//
#include <iostream>
#include <vector>

using namespace std;

inline void printInPairs(const vector<int>& arr, const int end) {
    // Print elements of arr[0:end] (non-inclusive end bound)
    // Should assert that end % 2 != 0 and is >= 3 to ensure no index out of bounds error
    for (int i = 0; i < end; i += 2) {
        cout << arr[i] + 1 << " " << arr[i + 1] + 1 << endl;
    }
}

int main() {
    int t, n, tmp;
    cin >> t;

    for (int i = 0; i < t; i++) {
        vector<int> evenIndices;
        vector<int> oddIndices;
        cin >> n;
        for (int j = 0; j < 2 * n; j++) {
            cin >> tmp;
            if (tmp % 2 == 0) {
                evenIndices.push_back(j);
            } else {
                oddIndices.push_back(j);
            }
        }

        if (evenIndices.size() % 2 == 1 && oddIndices.size() % 2 == 1) {
            printInPairs(evenIndices, evenIndices.size() - 1);
            printInPairs(oddIndices, oddIndices.size() - 1);
        } else if (evenIndices.size() > 0) {
            printInPairs(evenIndices, evenIndices.size() - 2);
            printInPairs(oddIndices, oddIndices.size());
        } else {
            printInPairs(oddIndices, oddIndices.size() - 2);
        }
    }
}
