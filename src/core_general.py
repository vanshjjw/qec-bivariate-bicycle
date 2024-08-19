import numpy as np
import src.helpers as helper
import src.group_helper as group_help
import src.validators as vd
import src.distances.distance_from_brute_force as brute_force
import src.distances.distance_from_generators as generators
import src.distances.distance_from_gap as qdistrand
import src.distances.distance_from_bposd as bposd
from src.graph_helper import TannerGraph


class BBCodeGeneral:
    def __init__(self, generators: list[str], relators: list[str], safe_mode: bool = False):
        self.relators = relators
        self.generators = generators
        self.safe_mode = safe_mode
        self.A_expression: list[str] = []
        self.B_expression: list[str] = []
        if self.safe_mode:
            self.validate_relators()

    def __int__(self, relators: list[str], safe_mode: bool = False):
        self.generators = ["x", "y"]
        self.relators = relators
        self.safe_mode = safe_mode
        self.A_expression: list[str] = []
        self.B_expression: list[str] = []
        if self.safe_mode:
            self.validate_relators()


    def validate_relators(self):
        extended_generators = self.generators + ["i"]
        for relator in self.relators:
            if all([r not in extended_generators for r in relator]):
                raise ValueError("Relator must contain at least one generator")
        return self


    def set_expression(self, A_expression: list[str], B_expression: list[str]):
        self.A_expression = A_expression
        self.B_expression = B_expression
        return self


    def find_distance(self, H_x, H_z, n, k, distance_method):
        if distance_method == 1:
            return brute_force.calculate_distance(H_x, H_z, n, k, status_updates=self.safe_mode)
        if distance_method == 2:
            return generators.calculate_distance(H_x, H_z, n, k, status_updates=self.safe_mode)
        if distance_method == 3:
            return qdistrand.calculate_distance(H_x, H_z, status_updates=self.safe_mode)
        if distance_method == 4:
            return bposd.calculate_distance(H_x, H_z, status_updates=self.safe_mode)


    def make_A_B_matrices(self):
        group = group_help.make_base_group(self.generators, self.relators)
        group_generators = group.gens()

        poly_variables = {}
        poly_variables["i"] = group([])
        for i, gen in enumerate(self.generators):
            poly_variables[gen] = group_generators[i]

        A_algebra_elements = group_help.make_elements_from_expressions(self.A_expression, poly_variables)
        B_algebra_elements = group_help.make_elements_from_expressions(self.B_expression, poly_variables)

        A_matrix = group_help.make_block_matrix(group, A_algebra_elements, action_is_right=False)
        B_matrix = group_help.make_block_matrix(group, B_algebra_elements, action_is_right=True)
        return A_matrix, B_matrix


    def create_parity_check_matrices(self):
        A, B = self.make_A_B_matrices()

        H_x = np.concatenate((A, B), axis=1)
        H_z = np.concatenate((B.T, A.T), axis=1)

        if self.safe_mode:
            vd.validate_parity_matrices(H_x, H_z)

        return H_x, H_z


    def generate_bb_code(self, distance_method = 0):
        H_x, H_z = self.create_parity_check_matrices()

        rank_H_x = helper.binary_rank(H_x)
        rank_H_z = helper.binary_rank(H_z)

        if self.safe_mode:
            vd.validate_ranks(rank_H_x, rank_H_z)

        # code parameters
        num_physical = 2 * len(H_x)
        num_logical = num_physical - rank_H_x - rank_H_z

        # no need to calculate distance
        if num_logical == 0 or distance_method == 0:
            return num_physical, num_logical, 0

        distance = self.find_distance(H_x, H_z, num_physical, num_logical, distance_method)

        return num_physical, num_logical, distance


    def make_graph(self):
        Hx, Hz = self.create_parity_check_matrices()
        Graph = TannerGraph(Hx, Hz)
        Graph.make_graph()
        return Graph




# Example input for polynomial expressions: ["x0", "x1", "y11", "x21.y21", "x3.y15"]






