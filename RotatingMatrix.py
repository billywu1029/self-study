A = [0xF, 0x8, 0x9, 0x7]
'''
A:
1111
1000
1001
0111

Desired:
0111
1001
1001
1101

'''
N = 4

# Circular shifts row r left by "shift" bits
def left_shift(A, r, shift):
    A[r] = (A[r] << shift | A[r] >> (N - shift)) & 0xF

# Circular shifts column c down by "c" bits
def down_shift(A):
    B = [0x0, 0x0, 0x0, 0x0]
    stay_mask = 0x9  # 1001
    for j in range(N):
        B[j] = (A[j] & stay_mask) | (A[(j + N - int(N/2)) % N] & ~stay_mask)
    print_bin(B)
    stay_mask = 0x5  # 0101
    for j in range(N):
        A[j] = (B[j] & stay_mask) | (B[(j + N - int(N/4)) % N] & ~stay_mask)

def print_bin(matrix):
    for row in matrix:
        print(bin(row))

print_bin(A)
for r in range(N):
    left_shift(A, r, r + 1)
print("\n")
print_bin(A)
print("B: ")

down_shift(A)
print("\n")
print_bin(A)

for r in range(N):
    left_shift(A, r, r)
print("\n")
print_bin(A)