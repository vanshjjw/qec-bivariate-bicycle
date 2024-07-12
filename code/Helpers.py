import numpy as np
import galois
from copy import deepcopy

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


def generate_binary_strings_in_order(i:int, n:int, arr):
    if i == n:
        yield arr
        return

    arr[i] = 0
    yield from generate_binary_strings_in_order(i + 1, n, arr)
    arr[i] = 1
    yield from generate_binary_strings_in_order(i + 1, n, arr)


def find_all_logical_operators(H_x, H_z, n, k, status_updates=False):
    all_operators = generate_binary_strings_in_order(0, 2 * n, np.zeros(2 * n, dtype=int))
    logical_operators = []
    rank = (n - k) // 2
    check = 0

    # print(f"n: {n}")
    # print(f"Rank: {rank}")
    # print(f"size of H_x: {H_x.shape} and H_z: {H_z.shape}")
    print(f"\nFinding all logical operators. Checking : {2 ** (2 * n)} operators.")

    for operator in all_operators:
        if not any(np.matmul(H_x, operator[:n]) % 2) and not any(np.matmul(H_z, operator[n:]) % 2):

            expanded_H_x = np.concatenate((H_x, np.array([operator[:n]])), axis=0)
            expanded_H_z = np.concatenate((H_z, np.array([operator[n:]])), axis=0)

            if calculate_rank_GF2(expanded_H_x) > rank or calculate_rank_GF2(expanded_H_z) > rank:
                logical_operators.append(deepcopy(operator))

        if status_updates and check % 50000 == 0:
            print(f"Checked {check} operators")
        check += 1

    print(f"Checked {check} operators. \nSearch complete.\n")
    return logical_operators


def calculate_distance_brute_force(H_x, H_z,  n, k, status_updates=False):
    logical_operators = find_all_logical_operators(H_x, H_z, n, k, status_updates)

    min_weight = 2 * n
    for operator in logical_operators:
        weight = sum([1 if operator[i] == 1 or operator[i + n] == 1 else 0 for i in range(n)])
        min_weight = min(min_weight, weight)

    return min_weight


