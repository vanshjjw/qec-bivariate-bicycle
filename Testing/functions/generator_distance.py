import numpy as np
from src.distances.distance_from_generators import generate_binary_combinations_for_generators


def check_binary_combinations_produce_right_number_of_operators(n: int, k: int) -> bool:
    num_found = 0
    all_operators = generate_binary_combinations_for_generators(0, n + k, n - k, np.zeros(n + k, dtype=int))
    for operator in all_operators:
            num_found += 1
    num_expected = 2 ** (n + k) -  2 ** (n - k)

    print(f"Number of operators found: {num_found} and expected: {num_expected}")



if __name__ == "__main__":
    num = 7
    logical = 6
    check_binary_combinations_produce_right_number_of_operators(num, logical)
    pass