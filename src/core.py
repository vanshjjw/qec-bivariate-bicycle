import numpy as np
import src.helpers as helper
import src.validators as vd
import src.distances.distance_from_brute_force as brute_force
import src.distances.distance_from_generators as generators
import src.distances.distance_from_gap as qdistrand
import src.distances.distance_from_bposd as bposd


class BBCode:
    def __init__(self, l: int, m: int, A_expression:list[str], B_expression: list[str], safe_mode = False):
        self.l = l
        self.m = m
        self.A_expression = A_expression
        self.B_expression = B_expression
        self.safe_mode = safe_mode
        self.poly_variables = {}

    def find_distance(self, H_x, H_z, n, k, distance_method):
        if distance_method == 1:
            return brute_force.calculate_distance(H_x, H_z, n, k, status_updates=self.safe_mode)
        if distance_method == 2:
            return generators.calculate_distance(H_x, H_z, n, k, status_updates=self.safe_mode)
        if distance_method == 3:
            return qdistrand.calculate_distance(H_x, H_z, status_updates=self.safe_mode)
        if distance_method == 4:
            return bposd.calculate_distance(H_x, H_z, status_updates=self.safe_mode)

    def create_poly_variables(self):
        # currently using the cyclic groups, and bivariate polynomials
        S_l = helper.create_matrix_S(self.l)
        S_m = helper.create_matrix_S(self.m)

        # Make x and y matrices
        self.poly_variables["i"] = np.eye(self.l * self.m, dtype=int)
        self.poly_variables["x"] = np.kron(S_l, np.eye(self.m, dtype=int))
        self.poly_variables["y"] = np.kron(np.eye(self.l, dtype=int), S_m)
        pass

    def construct_matrix_from_expression(self, expression: list[str]):
        size = self.l * self.m
        M = np.zeros((size, size), dtype=int)

        for elements in expression:
            p = np.eye(size, dtype=int)

            for elem in elements.split("."):
                if len(elem) == 1:
                    variable, exponent = elem, 1
                else:
                    variable, exponent = elem[0], int(elem[1:])
                p = p @ np.linalg.matrix_power(self.poly_variables[variable], exponent)

            M = (M + p) % 2

        return M

    def create_parity_check_matrices(self):
        # Create x and y matrices
        self.create_poly_variables()

        # Make A and B matrices
        A = self.construct_matrix_from_expression(self.A_expression)
        B = self.construct_matrix_from_expression(self.B_expression)

        H_x = np.concatenate((A, B), axis=1)
        H_z = np.concatenate((B.T, A.T), axis=1)

        if self.safe_mode:
            vd.validate_A_B_matrices(A, self.A_expression)
            vd.validate_A_B_matrices(B, self.B_expression)
            vd.validate_parity_matrix(H_x, H_z)
            print(f"H_x shape: {H_x.shape}")
            print(f"H_z shape: {H_z.shape}")
            print("\nParity matrices created successfully")
            pass

        return H_x, H_z

    def generate_bb_code(self, distance_method = 0):
        H_x, H_z = self.create_parity_check_matrices()

        rank_H_x = helper.binary_rank(H_x)
        rank_H_z = helper.binary_rank(H_z)

        if self.safe_mode:
            vd.validate_ranks(rank_H_x, rank_H_z)
            print(f"rank of H_x: {rank_H_x}")
            print(f"rank of H_z: {rank_H_z}")
            print("Rank of H_x and H_z validated successfully")

        # code parameters
        num_physical : int = 2 * self.l * self.m
        num_logical : int = num_physical - 2 * rank_H_x
        distance = 0

        # no need to calculate distance
        if num_logical == 0 or distance_method == 0:
            return num_physical, num_logical, distance

        distance = self.find_distance(H_x, H_z, num_physical, num_logical, distance_method)
        return num_physical, num_logical, distance



def single_run():
    A = {
        "l": 6,
        "m": 9,
        "a": ["x0", "y1", "y2"],
        "b": ["y3", "x2", "x4"],
        "answer": [[108, 16, 6]]
    }

    print(f"l: {A['l']}, m: {A['m']}")
    print(f"A: {A['a']}")
    print(f"B: {A['b']}")

    code = BBCode(A['l'], A['m'], A['a'], A['b'], safe_mode=True)
    n, k, d = code.generate_bb_code(distance_method=3)

    print(f"\nRequired BB code: [{n}, {k}, {d}]")
    if "answer" in A:
        print(f"answer: {A['answer']}")
    pass



def single_run_2():
    A = {
        'l': 10,
        'm': 10,
        'a': ['x0', 'x2', 'x4'],
        'b': ['y0', 'y2', 'y4'],
        'answer': [162, 24, 2]
    }

    print(f"l: {A['l']}, m: {A['m']}")
    print(f"A: {A['a']}")
    print(f"B: {A['b']}")

    code = BBCode(A['l'], A['m'], A['a'], A['b'], safe_mode=True)
    n, k, d = code.generate_bb_code(distance_method=3)

    print(f"\nRequired BB code: [{n}, {k}, {d}]")
    if "answer" in A:
        print(f"answer: {A['answer']}")



def single_run_3():
    A = {
        "l": 16,
        "m": 16,
        "a": ["x1", "y2"],
        "b": ["x1", "y2"],
    }

    print(f"l: {A['l']}, m: {A['m']}")
    print(f"A: {A['a']}")
    print(f"B: {A['b']}")

    code = BBCode(A['l'], A['m'], A['a'], A['b'], safe_mode=True)
    n, k, d = code.generate_bb_code(distance_method=3)

    print(f"\nRequired BB code: [{n}, {k}, {d}]")
    if "answer" in A:
        print(f"answer: {A['answer']}")

    pass




# Example inpt for polynomial expressions: ["x0", "x1", "y11", "x21.y21", "x3.y15"]
if __name__ == "__main__":
    single_run_3()






