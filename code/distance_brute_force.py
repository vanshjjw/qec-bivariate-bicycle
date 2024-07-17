import numpy as np
from copy import deepcopy
import Helpers as helper


def generate_all_binary_combinations(i:int, num_bits:int, arr) -> np.ndarray:
    if i == num_bits:
        yield arr
        return

    arr[i] = 0
    yield from generate_all_binary_combinations(i + 1, num_bits, arr)
    arr[i] = 1
    yield from generate_all_binary_combinations(i + 1, num_bits, arr)


def generate_all_binary_combinations_bbcode(i:int, num_bits:int, arr) -> np.ndarray:
    if i == num_bits:
        yield arr
        return

    if num_bits//4 <= i < num_bits//2:
        arr[i] = 0
        yield from generate_all_binary_combinations_bbcode(i + 1, num_bits, arr)
    else:
        arr[i] = 0
        yield from generate_all_binary_combinations_bbcode(i + 1, num_bits, arr)
        arr[i] = 1
        yield from generate_all_binary_combinations_bbcode(i + 1, num_bits, arr)



def find_all_logical_operators(H_x, H_z, n: int, k: int, status_updates=False) -> list[np.ndarray]:
    all_operators = generate_all_binary_combinations_bbcode(0, 2 * n, np.zeros(2 * n, dtype=int))
    logical_operators = []
    rank = (n - k) // 2
    check = 0

    if status_updates:
        print(f"\nFinding all logical operators. Checking : {2 ** (1.5 * n)} operators.")
        print(f"Estimated time: {2 ** (1.5 * n) / (10 ** 6) * 4} seconds\n")

    for operator in all_operators:
        if not any(np.matmul(H_x, operator[:n]) % 2) and not any(np.matmul(H_z, operator[n:]) % 2):

            expanded_H_x = np.concatenate((H_x, np.array([operator[:n]])), axis=0)
            expanded_H_z = np.concatenate((H_z, np.array([operator[n:]])), axis=0)

            if helper.calculate_rank_GF2(expanded_H_x) > rank or helper.calculate_rank_GF2(expanded_H_z) > rank:
                logical_operators.append(deepcopy(operator))

        if status_updates and check % 1000000 == 0:
            print(f"Checked {check} operators")
        check += 1

    if status_updates:
        print(f"Checked {check} operators. \nSearch complete.\n")
        print("Logical operators found: ", len(logical_operators))
    return logical_operators



def calculate_distance_brute_force(H_x, H_z,  n: int, k: int, status_updates=False) -> int:
    logical_operators = find_all_logical_operators(H_x, H_z, n, k, status_updates)

    min_weight = 2 * n
    for operator in logical_operators:
        weight = sum([1 if operator[i] == 1 or operator[i + n] == 1 else 0 for i in range(n)])
        min_weight = min(min_weight, weight)

    return min_weight



def check_binary_combinations_produce_correct_number(n: int, k: int) -> bool:
    num_found = 0
    all_operators = generate_all_binary_combinations_bbcode(0, 2 * n, np.zeros(2 * n, dtype=int))
    for operator in all_operators:
            print(operator)
            num_found += 1
    num_expected = int(2 ** (1.5 * n))

    print(f"Number of operators found: {num_found} and expected: {num_expected}")



if __name__ == "__main__":
    num = 4
    logical = 0
    check_binary_combinations_produce_correct_number(num, logical)
    pass