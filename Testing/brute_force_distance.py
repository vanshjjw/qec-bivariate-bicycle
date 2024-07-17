from src.distance_brute_force import generate_all_binary_combinations_bbcode
import numpy as np

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