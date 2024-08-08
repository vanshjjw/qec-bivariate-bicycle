from src.experimentation.propose_parameters import ProposeParameters
from src.polynomials import PolynomialToGraphs
from src.core import BBCode
import numpy as np
import src.helpers as helper
import networkx as nx


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
            # if i % 200 == 0 and i != 0:
            #     l = np.random.randint(8, 14)
            #     m = np.random.randint(8, 14)
            #     parameters = ProposeParameters(l, m)
            #     poly_graph = PolynomialToGraphs(l, m)
            #     print(f"New parameters: l = {l}, m = {m}")
            #     print("\n")

        # create base polynomials
        A, B = parameters.distribute_monomials(parameters.draw_random_monomials(num_x, num_y))
        code_1 = BBCode(l, m, A, B, safe_mode=False)
        n1, k1, d1 = code_1.generate_bb_code(distance_method=0)

        if k1 == 0:
            continue

        G_unique_1 = poly_graph.find_graph_generators(A, B, unique=True)
        is_connected_local = poly_graph.group_size(G_unique_1) == l * m

        if not is_connected_local:
            continue

        # base polynomials gives non-zero encoding and produces a connected graph...
        print(f"A: {A}, B: {B}")
        print(f"code: [{n1}, {k1}, {d1}]")
        print("\n")

        # square only A
        A2 = A
        B2 = poly_graph.poly_help.multiply_polynomials(B, B)

        code_2 = BBCode(l, m, A2, B2, safe_mode=False)
        n2, k2, d2 = code_2.generate_bb_code(distance_method=0)

        G_unique_2 = poly_graph.find_graph_generators(A2, B2, unique=True)
        graph_2 = code_2.graph()

        # print squared polynomials results
        print(f"A^2: {A2}, B^2: {B2}")
        print(f"code^2: [{n2}, {k2}, {d2}]")
        is_connected_local = poly_graph.group_size(G_unique_2) == l * m
        is_connected_global = helper.is_connected(graph_2)
        num_components = helper.num_connected_components(graph_2)

        if is_connected_local:
            print("Squared polynomials are connected")
            if not is_connected_global:
                print(f"NX disagrees with the local formula. Says it has {num_components} components")
                input("\nPress the <ENTER> key to continue...\n")
        else:
            print("Squared polynomials are not connected")
            if is_connected_global:
                print("NX disagrees with the local formula")
            else:
                print(f"Number of components in squared polynomials: {num_components}")

            print(f"Graph generators: {G_unique_2}")
            print(f"k increased by : {(k2 / k1)}, components by: {num_components}")
            if int(k2 / k1) != num_components:
                print("k increased by a different amount than the number of components")
                input("\nPress the <ENTER> key to continue...\n")
        print("\n")

        # cube the polynomials
        # A3 = poly_graph.poly_help.multiply_polynomials(A2, A)
        # B3 = poly_graph.poly_help.multiply_polynomials(B2, B)
        #
        # code_3 = BBCode(l, m, A3, B3, safe_mode=False)
        # n3, k3, d3 = code_3.generate_bb_code(distance_method=0)
        #
        # G_unique_3 = poly_graph.find_graph_generators(A3, B3, unique=True)
        #
        # # print cubed polynomials results
        # print(f"A^3: {A3}, B^3: {B3}")
        # print(f"code^3: [{n3}, {k3}, {d3}]")
        # is_connected = poly_graph.group_size(G_unique_3) == l * m
        # if is_connected:
        #     print("Cubed polynomials are connected")
        # else:
        #     components = helper.compute_sub_graphs(code_3.graph())
        #     print(f"Number of components in cubed polynomials: {len(components)}")
        #     print(f"k increased by : {(k3 / k1)}, components by: {len(components)}")
        #     program_pause = input("\nPress the <ENTER> key to continue...\n")

        print("\n\n\n")
        pass


if __name__ == "__main__":
    check()
