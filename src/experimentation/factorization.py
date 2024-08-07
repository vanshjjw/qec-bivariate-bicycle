from src.experimentation.propose_parameters import ProposeParameters
from src.polynomials import PolynomialToGraphs
from src.core import BBCode
import numpy as np
import src.helpers as helper



def check():
    l = 12
    m = 12
    num_shots = 1000
    num_x = 3
    num_y = 3
    parameters = ProposeParameters(l, m)
    poly_graph = PolynomialToGraphs(l, m)

    print("Square connected polynomials to see how code and graph components change")

    for i in range(num_shots):
        if i % 20 == 0:
            print(f"Trial {i} completed.")
            if i % 20000 == 0 and i != 0:
                l = np.random.randint(8, 14)
                m = np.random.randint(8, 14)
                parameters = ProposeParameters(l, m)
                poly_graph = PolynomialToGraphs(l, m)
                print(f"New parameters: l = {l}, m = {m}")
                print("\n")


        A, B = parameters.distribute_monomials(parameters.draw_random_monomials(num_x, num_y))
        code_1 = BBCode(l, m, A, B, safe_mode=False)
        n1, k1, d1 = code_1.generate_bb_code(distance_method=0)

        if k1 == 0:
            continue

        G_unique_1 = poly_graph.find_graph_generators(A, B, unique=True)
        is_connected = poly_graph.group_size(G_unique_1) == l * m

        if not is_connected:
            continue

        # base polynomial gives non-zero encoding and produces a connected graph...

        A2 = poly_graph.poly_help.multiply_polynomials(A, A)
        B2 = poly_graph.poly_help.multiply_polynomials(B, B)

        code_2 = BBCode(l, m, A2, B2, safe_mode=False)
        n2, k2, d2 = code_2.generate_bb_code(distance_method=0)

        G_unique_2 = poly_graph.find_graph_generators(A2, B2, unique=True)
        components = []

        print("\n")
        print(f"A: {A}, A^2: {A2}")
        print(f"B: {B}, `B^2: {B2}")
        print(f"code: [{n1}, {k1}, {d1}] goes to [{n2}, {k2}, {d2}]")
        print("\n")

        is_connected = poly_graph.group_size(G_unique_2) == l * m
        if is_connected:
            print("Squared polynomials are connected")
        else:
            components = helper.compute_sub_graphs(code_2.graph())
            print(f"Number of components in squared polynomials: {len(components)}")
            print(f"k increased by : {(k2 / k1)}, components by: {len(components)}")
            print(f"increase by same value: ", int(k2 / k1) == len(components))

        print("\n\n")


if __name__ == "__main__":
    check()
