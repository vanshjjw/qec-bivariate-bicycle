import numpy as np
from copy import deepcopy
import Helpers as helper


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

    if status_updates:
        print(f"\nFinding all logical operators. Checking : {2 ** (2 * n)} operators.")

    for operator in all_operators:
        if not any(np.matmul(H_x, operator[:n]) % 2) and not any(np.matmul(H_z, operator[n:]) % 2):

            expanded_H_x = np.concatenate((H_x, np.array([operator[:n]])), axis=0)
            expanded_H_z = np.concatenate((H_z, np.array([operator[n:]])), axis=0)

            if helper.calculate_rank_GF2(expanded_H_x) > rank or helper.calculate_rank_GF2(expanded_H_z) > rank:
                logical_operators.append(deepcopy(operator))

        if status_updates and check % 50000 == 0:
            print(f"Checked {check} operators")
        check += 1

    if status_updates:
        print(f"Checked {check} operators. \nSearch complete.\n")
    return logical_operators



def calculate_distance_brute_force(H_x, H_z,  n, k, status_updates=False):
    logical_operators = find_all_logical_operators(H_x, H_z, n, k, status_updates)

    min_weight = 2 * n
    for operator in logical_operators:
        weight = sum([1 if operator[i] == 1 or operator[i + n] == 1 else 0 for i in range(n)])
        min_weight = min(min_weight, weight)

    return min_weight