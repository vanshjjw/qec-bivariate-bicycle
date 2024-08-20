import numpy as np
import src.helpers.linalg_helpers as linalg_help
import src.misc.validators as vd
import src.distances.distance_from_brute_force as brute_force
import src.distances.distance_from_generators as generators
import src.distances.distance_from_gap as qdistrand
import src.distances.distance_from_bposd as bposd
from src.helpers.polynomials import PolynomialHelper
from src.helpers.graphs import TannerGraph

class BBCodeCached:
    def __init__(self, l: int, m: int, safe_mode = False):
        self.l = l
        self.m = m
        self.safe_mode = safe_mode
        self.A_expression = None
        self.B_expression = None
        self.H_x = None
        self.H_z = None
        self.poly_variables = {}
        self.poly_help = PolynomialHelper(l, m)
        self.create_cache()

    def set_expressions(self, A_expression: list[str], B_expression: list[str]):
        self.A_expression = A_expression
        self.B_expression = B_expression
        return self


    def find_distance(self, n, k, distance_method):
        distance_safe: bool = self.safe_mode and distance_method != 4
        if distance_method == 1:
            return brute_force.calculate_distance(self.H_x, self.H_z, n, k, status_updates=distance_safe)
        if distance_method == 2:
            return generators.calculate_distance(self.H_x, self.H_z, n, k, status_updates=distance_safe)
        if distance_method == 3:
            return qdistrand.calculate_distance(self.H_x, self.H_z, status_updates=distance_safe)
        if distance_method == 4:
            return bposd.calculate_distance(self.H_x, self.H_z, status_updates=distance_safe)


    def create_cache(self):
        # currently using the cyclic groups, and bivariate polynomials
        S_l = linalg_help.create_matrix_S(self.l)
        S_m = linalg_help.create_matrix_S(self.m)

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
        Answer: np.ndarray = np.zeros((size, size), dtype=int)
        powers: list[(int, int)] = self.poly_help.construct_powers_from_expression(expression)

        for power in powers:
            sub_matrix: np.ndarray = self.poly_variables["i1"]
            if power[0] != 0:
                sub_matrix = sub_matrix @ self.poly_variables[f"x{power[0]}"]
            if power[1] != 0:
                sub_matrix = sub_matrix @ self.poly_variables[f"y{power[1]}"]
            Answer = (Answer + sub_matrix) % 2

        return Answer


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
            vd.validate_parity_matrices(H_x, H_z)
            pass

        return H_x, H_z


    def generate_bb_code(self, distance_method = 0):
        H_x, H_z = self.create_parity_check_matrices()
        self.H_x = H_x
        self.H_z = H_z

        rank_H_x = linalg_help.binary_rank(H_x)
        rank_H_z = linalg_help.binary_rank(H_z)

        if self.safe_mode:
            vd.validate_ranks(rank_H_x, rank_H_z)

        # code parameters
        num_physical : int = 2 * self.l * self.m
        num_logical : int = num_physical - 2 * rank_H_x

        # no need to calculate distance
        if num_logical == 0 or distance_method == 0:
            return num_physical, num_logical, 0

        distance = self.find_distance(num_physical, num_logical, distance_method)

        return num_physical, num_logical, distance


    def make_graph(self):
        if self.H_x is None or self.H_z is None:
            self.H_x, self.H_z = self.create_parity_check_matrices()

        Graph = TannerGraph(self.H_x, self.H_z).set_l_and_m(self.l, self.m)
        Graph.add_nodes_and_edges()
        return Graph