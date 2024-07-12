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

    print(f"n: {n}")
    print(f"Rank: {rank}")
    print(f"size of H_x: {H_x.shape} and H_z: {H_z.shape}")
    print(f"Number of operators to check: {2 ** (2 * n)}")


    for operator in all_operators:
        if not any(np.matmul(H_x, operator[:n]) % 2) and not any(np.matmul(H_z, operator[n:]) % 2):
            print("Found a candidate operator")

            expanded_H_x = np.concatenate((H_x, np.array([operator[:n]])), axis=0)
            expanded_H_z = np.concatenate((H_z, np.array([operator[n:]])), axis=0)

            if calculate_rank_GF2(expanded_H_x) > rank or calculate_rank_GF2(expanded_H_z) > rank:
                logical_operators.append(operator)
                print("Found a logical operator")

        if status_updates and check % 50000 == 0:
            print(f"Checked {check} operators")
        check += 1

    return logical_operators


def calculate_distance_brute_force(H_x, H_z,  n, k, status_updates=False):
    logical_operators = find_all_logical_operators(H_x, H_z, n, k, status_updates)
    print(f"\nFound {len(logical_operators)} logical operators")
    min_weight = 2 * n
    min_operator = None

    for operator in logical_operators:
        weight = sum(operator)
        if weight < min_weight:
            min_weight = weight
            min_operator = operator
            print(f"New minimum weight: {min_weight}")

    return min_weight


