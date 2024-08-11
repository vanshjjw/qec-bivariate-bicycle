from src.polynomials import PolynomialHelper
from src.propose_parameters import ProposeParameters
from src.core import BBCode
import src.helpers as helper

def factors_as_strings(factors):
    i = 0
    s = ""
    for f, exp in zip(factors[0], factors[1]):
        s += f"{f}^{exp}"
        if i < len(factors[0]) - 1:
            s += "  *  "
        i += 1
    return s


def __check_and_print_code(l, m, a, b, check_k = False):
    code = BBCode(l, m, a, b)
    n, k, d = code.generate_bb_code(distance_method=3)

    print(f"New code: [{n}, {k}, {d}]")

    graph = code.graph()
    if helper.is_connected(graph):
        print("New graph is connected.")
    else:
        print(f"Number of components in new graph: {helper.num_connected_components(graph)}")
    print("\n")

    return k


# Factorize the disconnected polynomials to break down the code into connected components.
def factorize_disconnected_polynomials():
    l = 14
    m = 14
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
    num_shots = 1000

    zero_k = 0
    connected = 0

    for i in range(num_shots):
        if i % 50 == 0:
            print(f"{i}/{num_shots} completed.")
            print(f"No k value: {zero_k}/{i}")
            print(f"Connected: {connected}/{i - zero_k}")
            print("\n")

        A = parameters.draw_random_monomials(3, 0)
        B = parameters.draw_random_monomials(0, 3)

        code = BBCode(l, m, A, B)
        n, k, d = code.generate_bb_code(distance_method=3)

        if k == 0:
            zero_k += 1
            continue

        graph = code.graph()
        num_components = helper.num_connected_components(graph)
        is_connected = helper.is_connected(graph)

        if is_connected:
            connected += 1
            continue

        # base polynomials gives non-zero encoding and a disconnected graph

        A_Factors = poly_help.factorize(A, is_x=True)
        B_Factors = poly_help.factorize(B, is_x=False)

        print(f"Original polynomials. A : {A}, B : {B}")
        print(f"Original code: [{n}, {k}, {d}]")
        print(f"Number of components in original graph: {num_components}")
        print(f"Factorization of A: {factors_as_strings(A_Factors)}")
        print(f"Factorization of B: {factors_as_strings(B_Factors)}")
        print("\n")

        k_cumulative = 0

        for i, a in enumerate(A_Factors[0]):
            for j, b in enumerate(B_Factors[0]):

                code = BBCode(l, m, a, b)
                n, k, d = code.generate_bb_code(distance_method=3)

                print(f"checking factors a{i} and b{j}: code [{n}, {k}, {d}]")

                k_for_factors = k * A_Factors[1][i] * B_Factors[1][j]
                k_cumulative += k_for_factors

        print(f"cumulative k: {k_cumulative}, original k: {k}")
        print("-------------\n\n")



# Factorize the connected polynomials to break down the code into connected components.
def factorize_connected_polynomials():
    l = 14
    m = 14
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
    num_shots = 1000

    zero_k = 0
    disconnected = 0

    for i in range(num_shots):
        if i % 50 == 0:
            print(f"{i}/{num_shots} completed.")
            print(f"No k value: {zero_k}/{i}")
            print(f"Disconnected: {disconnected}/{i - zero_k}")
            print("\n")

        A = parameters.draw_random_monomials(3, 0)
        B = parameters.draw_random_monomials(0, 3)

        code = BBCode(l, m, A, B)
        n, k, d = code.generate_bb_code(distance_method=4)

        if k == 0:
            zero_k += 1
            continue

        graph = code.graph()
        is_connected = helper.is_connected(graph)

        if not is_connected:
            disconnected += 1
            continue

        # base polynomials gives non-zero encoding and connected graph

        A_Factors = poly_help.factorize(A, is_x=True)
        B_Factors = poly_help.factorize(B, is_x=False)

        print(f"Original polynomials. A : {A}, B : {B}")
        print(f"Original code: [{n}, {k}, {d}]")
        print(f"Factorization of A: {factors_as_strings(A_Factors)}")
        print(f"Factorization of B: {factors_as_strings(B_Factors)}")
        print("\n")

        k_cumulative = 0
        for a, power_a in zip(A_Factors[0], A_Factors[1]):
            for b, power_b in zip(B_Factors[0], B_Factors[1]):

                a_new = poly_help.raise_polynomial_to_power(a, power_a)
                b_new = poly_help.raise_polynomial_to_power(b, power_b)
                k_new = __check_and_print_code(l, m, a_new, b_new)

        print("-------------------\n\n")




if __name__ == "__main__":
    factorize_disconnected_polynomials()
    factorize_connected_polynomials()
    pass