import numpy as np


# Find all possible combinations of logical operators, multiplied by stabilizers
def generate_binary_combinations_for_generators(i:int, num_bits:int, num_stabilizers: int, arr) -> np.ndarray:
    if i == num_bits:
        if sum(arr[num_stabilizers:]) == 0:
            return
        else:
            yield arr
            return

    arr[i] = 0
    yield from generate_binary_combinations_for_generators(i + 1, num_bits, num_stabilizers, arr)
    arr[i] = 1
    yield from generate_binary_combinations_for_generators(i + 1, num_bits, num_stabilizers, arr)



def check_binary_combinations_produce_right_number_of_operators(n: int, k: int) -> bool:
    num_found = 0
    all_operators = generate_binary_combinations_for_generators(0, n + k, n - k, np.zeros(n + k, dtype=int))
    for operator in all_operators:
            num_found += 1
    num_expected = 2 ** (n + k) -  2 ** (n - k)

    print(f"Number of operators found: {num_found} and expected: {num_expected}")



def generate_all_logicals():
    pass













if __name__ == "__main__":
    n = 7
    k = 6
    check_binary_combinations_produce_right_number_of_operators(n, k)
    pass
