import numpy as np
import Helpers as helper
import Validators as vd

def create_parity_check_matrices(l: int, m: int, A_expression:list[(str, int)], B_expression: list[(str, int)]):
    S_l = helper.create_matrix_S(l)
    S_m = helper.create_matrix_S(m)

    # Make x and y matrices
    x = np.kron(S_l, np.eye(m, dtype=int))
    y = np.kron(np.eye(l, dtype=int), S_m)

    # vd.validate_x_y_matrices(x)
    # vd.validate_x_y_matrices(y)

    # Make A and B matrices
    A = np.zeros((l * m, l * m), dtype=int)
    B = np.zeros((l * m, l * m), dtype=int)

    for var, val in A_expression:
        A += np.linalg.matrix_power(x, val) if var == 'x' else np.linalg.matrix_power(y, val)
    for var, val in B_expression:
        B += np.linalg.matrix_power(x, val) if var == 'x' else np.linalg.matrix_power(y, val)

    # vd.validate_A_B_matrices(A, l, m, A_expression)
    # vd.validate_A_B_matrices(B, l, m, B_expression)

    H_x = np.concatenate((A, B), axis=1)
    H_z = np.concatenate((B.T, A.T), axis=1)

    # vd.validate_parity_matrix(H_x, H_z)

    return H_x, H_z






def generate_bb_code(l: int, m: int, a: list[(str, int)], b: list[(str, int)]):
    # calculate parity check matrices
    H_x, H_z = create_parity_check_matrices(l, m, a, b)

    # calculate rank
    rank_H_x = helper.calculate_rank_GF2(H_x)
    rank_H_z = helper.calculate_rank_GF2(H_z)

    print(f"Rank of H_x: {rank_H_x}")
    print(f"Rank of H_z: {rank_H_z}")

    vd.validate_rank(rank_H_x, rank_H_z)

    # code parameters
    num_physical : int = 2 * l * m
    num_logical : int = num_physical - 2 * rank_H_x
    distance : int = calculate_distance_brute_force(H_x, H_z, num_physical, num_logical)

    return num_physical, num_logical, distance



def main():
    A = {
        "l": 6,
        "m": 6,
        "a": [("x", 3), ("y", 1), ("y", 2)],
        "b": [("y", 3), ("x", 1), ("x", 2)],
        "answer": [72, 36, 6]
    }

    l = A["l"]
    m = A["m"]
    a = A["a"]
    b = A["b"]

    n, k, d = generate_bb_code(l, m, a, b)

    print(f"obtained: [{n}, {k}, {d}]")
    print(f"answer: {A['answer']}")



if __name__ == "__main__":
    main()








