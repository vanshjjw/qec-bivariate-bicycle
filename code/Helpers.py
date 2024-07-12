import numpy as np
import galois

def display(M, middle_line = False):
    size = len(M[0])

    h_line = "--" * size
    print(h_line)

    for row in M:
        print("[ ", end = "")
        for i in range(size):
            print(row[i], end = " ")
            if middle_line and i == size / 2:
                print("|", end = " ")
        print("]")

    print(h_line)
    pass


def create_matrix_S(size):
    S = np.eye(size, dtype=int, k = 1)
    S[size - 1][0] = 1
    return S


def calculate_rank_GF2(A):
    GF = galois.GF(2)
    rank = np.linalg.matrix_rank(GF(A))
    return rank

def generators(A):
    GF2 = galois.GF(2)
    A = GF2(A)
    rref_matrix, pivots = A.rref()
    return rref_matrix[~np.all(rref_matrix == 0, axis=1)]

def generate_binary_strings_in_order(i:int, n:int, arr):
    if i == n:
        yield arr
        return

    arr[i] = 0
    yield from generate_binary_strings_in_order(i + 1, n, arr)
    arr[i] = 1
    yield from generate_binary_strings_in_order(i + 1, n, arr)


def calculate_distance_brute_force(H_x, H_z,  n, k):
    all_operators = generate_binary_strings_in_order(0, 2 * n, np.zeros(2 * n, dtype=int))

    for operator in all_operators:
        if not any(operator):
            continue
        if not any(np.matmul(H_x, operator[:n]) % 2) and not any(np.matmul(H_z, operator[n:]) % 2):
            print("Found a candidate operator")

    return 0
