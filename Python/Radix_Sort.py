"""
Radix Sort:
Given list of integers that are not too large,
sort them not via traditional comparisons (would be bounded by
O(n log n) runtime), but instead by clever stable sorts from
the least significant digit to the most significant digit, leading
to O(n) performance. (Counting sort subroutine runtime suffers though
if the max number in the list is very large, or if base is large)

Author: Bill Wu
Date: Aug 4, 2019
"""

# Plan:
# RADIX SORT:
# Given array, parse entire arr, assert that every element is an integer
# Sort in place, so keep original array and modify it with each iteration
# Find max, num iters == num digits, ie log(max(A))
    # Each iter, invoke counting_sort subroutine on the numbers given, sorting
    # according to the curr digit
# Return sorted list at the end

# COUNTING SORT:
# Form b bins, where b == base of the system (default is 10)
# Order taken out of bin is very important to maintain stability during sort
# Want "smallest"/earliest seen of the nums in bin to come out first in sorted arr


def radix_sort(A, base=10):
    """
    :param A: Input array to be sorted
    :param base: Base of the numbers in the array, default to decimal base 10
    :return: Modified version of A that is sorted least to greatest
    """
    if not A:
        return A
    if not all([isinstance(x, int) for x in A]):
        raise Exception("Not all elements of the array are integers!")

    n_digits = len(str(max(A)))
    # Convert all numbers to strings to make indexing by digit easier
    A = list(map(str, A))

    tmp_arr = A[:]
    for i in range(1, n_digits+1):  # Want least significant to most significant, so use neg indices
        tmp_arr = counting_sort(tmp_arr, base, -i)  # negative to count from LSB

    return list(map(int, tmp_arr))


def counting_sort(A, base, curr_index):
    """
    :param A: Input array to be sorted, array of strings
    :param base: Base of the numbers in the array, default to decimal base 10
    :param currIdx: Index of digit that the sort should be conducted by
    :return: Sorted copy of A acc to currIdx digits in each number, (if no num in digit, assume '0')
    """
    result = []
    bins = [[] for _ in range(base)]
    for i, num in enumerate(A):
        try:
            bins[int(num[curr_index])].append(num)  # Try to get digit at currIdx and put to corresponding bin
        except IndexError:
            bins[0].append(num)  # Since the number of digits available < # digits(max num)

    for b in bins:  # Go through them in order from bin_0 to bin_base
        for j in b:  # For each element put in this bin
            result.append(j)  # ***** MAY NEED TO REVERSE LIST/DO STH FANCY HERE ******

    return result

arr = [23,62,63,9, 103, 128,2, 6,61,45,100,67,43, 1001, 5000000000]
arr = radix_sort(arr)
print(arr)


# Application of radix sort -
# Given n integers in a list, determine how many numbers fall within the range [a, b]

# Idea: Sort input array via radix sort (since all ints), then binary search for the index of both ends
# of the range, then return the difference between the indices
# Binary Search:
# Assume sorted array, continually halve the search space depending on if number is < or > guess

def nums_in_range(L, a, b):
    """
    :param L: Input list, contains n integers
    :param a: lower bound of range, int, inclusive (if lower bound in L, then will be included in the final count)
    :param b: upper bound of range, int, exclusive, must be different than a
    :return: Number of elements within this range [a, b]
    """
    assert a != b
    arr = radix_sort(L)
    ai = binary_search(arr, a, 0, len(arr), False)
    bi = binary_search(arr, b, 0, len(arr), True)

    return bi - ai

def binary_search(L, target, left, right, upper):
    """
    :param L: Input list, assume sorted
    :param target: Target int to look for
    :param left: lower bound, inclusive
    :param right: upper bound, exclusive
    :param upper: Type of bound is upper bound, bool; need this to decide whether to -/+ 1 for return index
    :return: Index of closest estimate to target
    """
    if left == right or right-left == 1:
        if upper:
            # Since upper bound is exclusive, exclude right/get right-1 if L[right-1] >= target
            if L[right-1] < target:
                return right  # L[right] fell within the upper bound of target, so include this index
            else:
                return right - 1
        else:
            # Since lower bound is inclusive, include left index if L[left] >= target
            if L[left] >= target:
                return left
            else:
                return left + 1

    i = (right-left) // 2
    if L[i+left] == target:
        return i+left
    elif L[i+left] < target:
        return binary_search(L, target, left + i, right, upper)
    else:
        return binary_search(L, target, left, right - i, upper)

def ins_sort(k):
    # Standard O(n^2) insertion sort
    for i in range(1,len(k)):
        j = i
        temp = k[j]
        while j > 0 and temp < k[j-1]:
            k[j] = k[j-1]
            j=j-1
        k[j] = temp
    return k

if __name__=="__main__":
    print("testing number of elements that fall in a range:")
    lis = [1, 23, 4, 5, 8, 3, 16, 11]
    lower_bound_inc = 1
    upper_bound_noninc = 8
    print("starting array: ", lis)
    print("array sorted w Radix sort: ", radix_sort(lis))
    print("number of elements between %r inclusive and %r exclusive: %r"
          % (lower_bound_inc, upper_bound_noninc, nums_in_range(lis, lower_bound_inc, upper_bound_noninc)))

    print("test #2")
    arr = [23,62,63,9, 103, 128,2, 6,61,45,100,67,43, 1001, 5000000000]
    r = (28, 110)
    print(arr)
    print(r)
    print(nums_in_range(arr, r[0], r[1]))

    print("\n\nSpeed test between Radix Sort and Insertion Sort on worst case input for insertion sort")
    arr = list(range(10000, -1, -1))
    import time
    t = time.time()

    ins_sort(arr)

    tend = time.time()
    print("Time taken with insertion sort: %r s" % (tend-t))

    tt = time.time()
    radix_sort(arr)
    ttend = time.time()
    print("Time taken with radix sort: %r s" % (ttend-tt))

