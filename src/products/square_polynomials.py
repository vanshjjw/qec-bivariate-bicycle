from src.propose_parameters import ProposeParameters
from src.polynomials import PolynomialToGraphs
from src.core import BBCode
from src.core_cached import BBCodeCached
import numpy as np
import src.helpers as helper


def change_parameters():
    l = np.random.randint(8, 14)
    m = np.random.randint(8, 14)
    parameters = ProposeParameters(l, m)
    poly_graph = PolynomialToGraphs(l, m)
    code_cached = BBCodeCached(l, m)
    print(f"New parameters: l = {l}, m = {m}")
    print("\n")
    return parameters, poly_graph, code_cached


def square_connected_polynomials():
    l = 12
    m = 12
    num_shots = 10000
    num_x = 3
    num_y = 3
    parameters = ProposeParameters(l, m)
    poly_graph = PolynomialToGraphs(l, m)
    code_cached = BBCodeCached(l, m)

    zero_k = 0

    print("Square connected polynomials to see how code and graph components change")

    for i in range(num_shots):
        # print progress
        if i % 50 == 0:
            print(f"{i}/{num_shots} completed.")
            print(f"No k value: {zero_k}/{i}")
            print("\n")

        # change parameters every 200 shots
        if i % 200 == 0 and i != 0:
            parameters, poly_graph, code_cached = change_parameters()

        # create base polynomials
        A, B = parameters.distribute_monomials(parameters.draw_random_monomials(num_x, num_y))
        n1, k1, d1 = code_cached.set_expressions(A, B).generate_bb_code(distance_method=4)

        if k1 == 0:
            zero_k += 1
            continue

        graph_1 = code_cached.graph()
        num_components_1 = helper.num_connected_components(graph_1)

        # base polynomials gives non-zero k
        print(f"A: {A}, B: {B}")
        print(f"code: [{n1}, {k1}, {d1}]")
        print(f"Number of components in original polynomials: {num_components_1}")
        print("\n")

        ### square polynomials
        A2 = poly_graph.poly_help.multiply_polynomials(A, A)
        B2 = poly_graph.poly_help.multiply_polynomials(B, B)

        n2, k2, d2 = code_cached.set_expressions(A2, B2).generate_bb_code(distance_method=4)
        graph_2 = code_cached.graph()
        num_components_2 = helper.num_connected_components(graph_2)

        # print squared polynomials results
        print(f"new code: [{n2}, {k2}, {d2}]")
        print(f"Number of components in squared polynomials: {num_components_2}")

        print("\n")
        print(f"k increased by : {(k2 / k1)}", end=": ")
        print(f"components increased by: {num_components_2 / num_components_1}")

        increase_equally = (k2 / k1) == (num_components_2 / num_components_1)

        if num_components_2 == 1:
            print("Squared polynomials are connected", end=": ")
            if increase_equally:
                print("conjecture passes")
            else:
                print("conjecture fails")
        else:
            print("Squared polynomials are disconnected", end=": ")
            if increase_equally:
                print("conjecture passes")
            else:
                print("conjecture fails")
        print("\n")

        print("------------\n\n")


if __name__ == "__main__":
    square_connected_polynomials()
