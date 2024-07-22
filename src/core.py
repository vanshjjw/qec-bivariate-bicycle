import numpy as np
import src.helpers as helper
import src.validators as vd
import src.distance_brute_force as dis_brute
import src.distance_from_generators as dis_gen
import src.distance_from_gap as dis_gap


def create_matrix_S(size):
    S = np.eye(size, dtype=int, k=1)
    S[size - 1][0] = 1
    return S


class BBCode:
    def __init__(self, l: int, m: int, A_expression:list[str], B_expression: list[str], debug = False):
        self.l = l
        self.m = m
        self.A_expression = A_expression
        self.B_expression = B_expression
        self.debug_mode = debug


    def construct_matrix_from_expression(self, expression: list[str], x: np.ndarray, y: np.ndarray):
        size = self.l * self.m
        M = np.zeros((size, size), dtype=int)

        for elements in expression:
            p = np.eye(size, dtype=int)
            for elem in elements.split("."):
                variable, exponent = elem[0], int(elem[1:])
                match variable:
                    case "x":
                        p = p @ np.linalg.matrix_power(x, exponent)
                    case "y":
                        p = p @ np.linalg.matrix_power(y, exponent)
            M = (M + p) % 2

        return M

    def create_parity_check_matrices(self):
        S_l = create_matrix_S(self.l)
        S_m = create_matrix_S(self.m)

        # Make x and y matrices
        x = np.kron(S_l, np.eye(self.m, dtype=int))
        y = np.kron(np.eye(self.l, dtype=int), S_m)

        # Make A and B matrices
        A = self.construct_matrix_from_expression(self.A_expression, x, y)
        B = self.construct_matrix_from_expression(self.B_expression, x, y)

        H_x = np.concatenate((A, B), axis=1)
        H_z = np.concatenate((B.T, A.T), axis=1)

        if self.debug_mode:
            vd.validate_x_y_matrices(x)
            vd.validate_x_y_matrices(y)
            vd.validate_A_B_matrices(A, self.A_expression)
            vd.validate_A_B_matrices(B, self.B_expression)
            vd.validate_parity_matrix(H_x, H_z)
            print(f"H_x shape: {H_x.shape}")
            print(f"H_z shape: {H_z.shape}")
            print("\nParity matrices created successfully")

        return H_x, H_z

    def generate_bb_code(self, distance_method=0):
        H_x, H_z = self.create_parity_check_matrices()

        rank_H_x = helper.binary_rank(H_x)
        rank_H_z = helper.binary_rank(H_z)
        print(f"Rank of H_x: {rank_H_x}")
        print(f"Rank of H_z: {rank_H_z}")

        if self.debug_mode:
            vd.validate_rank(rank_H_x, rank_H_z)

        # src parameters
        num_physical : int = 2 * self.l * self.m
        num_logical : int = num_physical - 2 * rank_H_x
        distance = 0

        if distance_method == 1:
            distance = dis_gen.calculate_distance(H_x, H_z, num_physical, num_logical, rank_H_x, rank_H_z, status_updates=True)
        elif distance_method == 2:
            distance = dis_brute.calculate_distance_brute_force(H_x, H_z, num_physical, num_logical, status_updates=True)
        elif distance_method == 3:
            distance = dis_gap.calculate_distance(H_x, H_z, status_updates=True)


        return num_physical, num_logical, distance



def single_run():
    A = {
        "l": 6,
        "m": 9,
        "a": ["x0", "y1", "y2"],
        "b": ["y3", "x2", "x4"],
        "answer": [[108, 16, 6]]
    }

    l = A["l"]
    m = A["m"]
    a = A["a"]
    b = A["b"]

    print(f"l: {l}, m: {m}")
    print(f"A: {a}")
    print(f"B: {b}")

    code = BBCode(l, m, a, b, debug=True)
    n, k, d = code.generate_bb_code(distance_method=3)

    print(f"\nRequired BB code: [{n}, {k}, {d}]")
    if "answer" in A:
        print(f"answer: {A['answer']}")


def single_run_2():
    pass



def single_run_3():
    A = {
        "l": 6,
        "m": 9,
        "a": ["x3", "y1", "y2"],
        #"b": ["y3", "x2", "x4"],
        "b": ["x3", "y1", "y2"],
        "answer": [[108, 16, 6]]
    }

    l = A["l"]
    m = A["m"]
    a = A["a"]
    b = A["b"]

    print(f"l: {l}, m: {m}")
    print(f"A: {a}")
    print(f"B: {b}")

    code = BBCode(l, m, a, b, debug=True)
    n, k, d = code.generate_bb_code(distance_method=3)

    print(f"\nRequired BB code: [{n}, {k}, {d}]")
    if "answer" in A:
        print(f"answer: {A['answer']}")




# Example inpt for polynomial expressions: ["x0", "x1", "y11", "x21.y21", "x3.y15"]
if __name__ == "__main__":
    single_run()






