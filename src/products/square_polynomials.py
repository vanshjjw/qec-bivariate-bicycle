from src.propose_parameters import ProposeParameters
from src.polynomial_helper import PolynomialHelper
from src.core import BBCode
from src.core_cached import BBCodeCached
import numpy as np
import src.helpers as helper


def change_parameters():
    l = np.random.randint(8, 14)
    m = np.random.randint(8, 14)
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
    code_cached = BBCodeCached(l, m)
    print(f"New parameters: l = {l}, m = {m}")
    print("\n")
    return parameters, poly_help, code_cached


def square_al_polynomials():
    l = 12
    m = 12
    num_shots = 10000
    num_x = 3
    num_y = 3
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
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
            parameters, poly_help, code_cached = change_parameters()

        # create base polynomials
        A, B = parameters.distribute_monomials(parameters.draw_random_monomials(num_x, num_y))
        n1, k1, d1 = code_cached.set_expressions(A, B).generate_bb_code(distance_method=3)

        if k1 == 0:
            zero_k += 1
            continue

        graph_1 = code_cached.make_graph()
        num_components_1 = graph_1.number_connected_components()

        ### square polynomials
        A2 = poly_help.multiply_polynomials(A, A)
        B2 = poly_help.multiply_polynomials(B, B)

        n2, k2, d2 = code_cached.set_expressions(A2, B2).generate_bb_code(distance_method=3)
        graph_2 = code_cached.make_graph()
        num_components_2 = graph_2.number_connected_components()

        increase_equally = (k2 / k1) == (num_components_2 / num_components_1)

        if not increase_equally:
            # base polynomials gives non-zero k
            print("\n")
            print(f"A: {A}, B: {B}")
            print(f"code: [{n1}, {k1}, {d1}]")
            print(f"Number of components in original polynomials: {num_components_1}")
            print("\n")

            # print squared polynomials results
            print(f"new code: [{n2}, {k2}, {d2}]")
            print(f"Number of components in squared polynomials: {num_components_2}")
            print("\n")
            print(f"k increased by : {(k2 / k1)}", end=": ")
            print(f"components increased by: {num_components_2 / num_components_1}")
            print("------------\n\n")
        else:
            which_one = "connected" if num_components_2 == 1 else "disconnected"
            print(f"conjecture holds for {which_one} polynomials")



def cheeky_examples():
    # A = ['x2', 'y11', 'x9']
    # B = ['y8', 'y9', 'x5']
    # code: [288, 12, 20]
    # Number of components in original polynomials: 1
    #
    # new code: [288, 32, 6]
    # Number of components in squared polynomials: 4
    #
    # k increased by : 2.6666666666666665: components increased by: 4.0
    # Squared polynomials are disconnected: conjecture fails
    pass



if __name__ == "__main__":
    cheeky_examples()
    pass






