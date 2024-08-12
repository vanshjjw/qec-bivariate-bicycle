import numpy as np
import src.helpers as helper
import src.validators as vd
import src.distances.distance_from_brute_force as brute_force
import src.distances.distance_from_generators as generators
import src.distances.distance_from_gap as qdistrand
import src.distances.distance_from_bposd as bposd


class BBCodeCached:
    def __init__(self, l: int, m: int, safe_mode = False):
        self.l = l
        self.m = m
        self.safe_mode = safe_mode
        self.A_expression = None
        self.B_expression = None
        self.poly_variables = {}
        self.create_cache()

    def set_expressions(self, A_expression: list[str], B_expression: list[str]):
        self.A_expression = A_expression
        self.B_expression = B_expression
        return self


    def find_distance(self, H_x, H_z, n, k, distance_method):
        distance_safe: bool = self.safe_mode and distance_method != 4
        if distance_method == 1:
            return brute_force.calculate_distance(H_x, H_z, n, k, status_updates=distance_safe)
        if distance_method == 2:
            return generators.calculate_distance(H_x, H_z, n, k, status_updates=distance_safe)
        if distance_method == 3:
            return qdistrand.calculate_distance(H_x, H_z, status_updates=distance_safe)
        if distance_method == 4:
            return bposd.calculate_distance(H_x, H_z, status_updates=distance_safe)


    def create_cache(self):
        # currently using the cyclic groups, and bivariate polynomials
        S_l = helper.create_matrix_S(self.l)
        S_m = helper.create_matrix_S(self.m)

        # basis matrices
        self.poly_variables["i1"] = np.eye(self.l * self.m, dtype=int)
        self.poly_variables["x1"] = np.kron(S_l, np.eye(self.m, dtype=int))
        self.poly_variables["y1"] = np.kron(np.eye(self.l, dtype=int), S_m)

        # all matrices
        for i in range(2, self.l):
            self.poly_variables[f"x{i}"] = self.poly_variables[f"x{i-1}"] @ self.poly_variables["x1"]
        for i in range(2, self.m):
            self.poly_variables[f"y{i}"] = self.poly_variables[f"y{i-1}"] @ self.poly_variables["y1"]

        if self.safe_mode:
            for key, value in self.poly_variables.items():
                vd.validate_x_y_matrices(value)
        pass


    def construct_matrix_from_expression(self, expression: list[str]):
        size = self.l * self.m
        M = np.zeros((size, size), dtype=int)

        for elements in expression:
            p = np.eye(size, dtype=int)

            for elem in elements.split("."):
                if len(elem) == 1:
                    p = p @ self.poly_variables[elem + "1"]
                else:
                    if elem[1:] != "0":
                        p = p @ self.poly_variables[elem]

            M = (M + p) % 2

        return M


    def create_parity_check_matrices(self):
        # Make A and B matrices
        if self.A_expression is None or self.B_expression is None:
            raise ValueError("A and B expressions must be set before creating parity check matrices")

        A = self.construct_matrix_from_expression(self.A_expression)
        B = self.construct_matrix_from_expression(self.B_expression)

        H_x = np.concatenate((A, B), axis=1)
        H_z = np.concatenate((B.T, A.T), axis=1)

        if self.safe_mode:
            vd.validate_A_B_matrices(A, self.A_expression)
            vd.validate_A_B_matrices(B, self.B_expression)
            vd.validate_parity_matrix(H_x, H_z)
            pass

        return H_x, H_z


    def generate_bb_code(self, distance_method = 0):
        H_x, H_z = self.create_parity_check_matrices()

        rank_H_x = helper.binary_rank(H_x)
        rank_H_z = helper.binary_rank(H_z)

        if self.safe_mode:
            vd.validate_ranks(rank_H_x, rank_H_z)

        # code parameters
        num_physical : int = 2 * self.l * self.m
        num_logical : int = num_physical - 2 * rank_H_x

        # no need to calculate distance
        if num_logical == 0 or distance_method == 0:
            return num_physical, num_logical, 0

        distance = self.find_distance(H_x, H_z, num_physical, num_logical, distance_method)

        return num_physical, num_logical, distance


    def graph(self):
        Hx, Hz = self.create_parity_check_matrices()
        return helper.make_graph(Hx, Hz)