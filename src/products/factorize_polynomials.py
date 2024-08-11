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

    for shot in range(num_shots):
        if shot % 50 == 0:
            print(f"{shot}/{num_shots} completed.")
            print(f"No k value: {zero_k}/{shot}")
            print(f"Connected: {connected}/{shot - zero_k}")
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

        k_cumulative_base = 0
        k_cumulative_raised = 0
        non_zero_codes = 0

        for i, a in enumerate(A_Factors[0]):
            for j, b in enumerate(B_Factors[0]):

                code = BBCode(l, m, a, b)
                n2, k2, d2 = code.generate_bb_code(distance_method=3)
                num_components = helper.num_connected_components(code.graph())
                print(f"checking factors a{i} and b{j}: code [{n2}, {k2}, {d2}]: has {num_components} components.")

                if k2 == 0:
                    continue
                else:
                    non_zero_codes += 1

                a_power = A_Factors[1][i]
                b_power = B_Factors[1][j]

                if a_power == 1 and b_power == 1:
                    continue

                a_raised = poly_help.raise_polynomial_to_power(a, a_power)
                b_raised = poly_help.raise_polynomial_to_power(b, b_power)

                code = BBCode(l, m, a_raised, b_raised)
                n3, k3, d3 = code.generate_bb_code(distance_method=3)
                num_components_3 = helper.num_connected_components(code.graph())
                print(f"checking factors a{i}^{a_power} and b{j}^{b_power}: code [{n3}, {k3}, {d3}]: has {num_components_3} components.")
                print(f"num_components_2 and powers: {num_components_3 == (a_power * b_power)}")
                print("\n")

                k_cumulative_base = k_cumulative_base + (k2 * a_power * b_power)
                k_cumulative_raised = k_cumulative_raised + k3

        print(f"k original: {k}, k cumulative base: {k_cumulative_base}, k cumulative raised: {k_cumulative_raised}")
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

    for shot in range(num_shots):
        if shot % 50 == 0:
            print(f"{shot}/{num_shots} completed.")
            print(f"No k value: {zero_k}/{shot}")
            print(f"Disconnected: {disconnected}/{shot - zero_k}")
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

        k_cumulative_base = 0
        k_cumulative_raised = 0
        non_zero_codes = 0

        for i, a in enumerate(A_Factors[0]):
            for j, b in enumerate(B_Factors[0]):

                code = BBCode(l, m, a, b)
                n2, k2, d2 = code.generate_bb_code(distance_method=3)
                num_components_2 = helper.num_connected_components(code.graph())
                print(f"checking factors a{i} and b{j}: code [{n2}, {k2}, {d2}]: has {num_components_2} components.")


                if k2 == 0:
                    continue

                non_zero_codes += 1
                a_power = A_Factors[1][i]
                b_power = B_Factors[1][j]

                if a_power == 1 and b_power == 1:
                    continue

                a_raised = poly_help.raise_polynomial_to_power(a, a_power)
                b_raised = poly_help.raise_polynomial_to_power(b, b_power)

                code = BBCode(l, m, a_raised, b_raised)
                n3, k3, d3 = code.generate_bb_code(distance_method=3)
                num_components_3 = helper.num_connected_components(code.graph())
                print(f"checking factors a{i}^{a_power} and b{j}^{b_power}: code [{n3}, {k3}, {d3}]: has {num_components_3} components.")
                print(f"num_components_2 and powers: {num_components_3 == (a_power * b_power)}")
                print("\n")

                k_cumulative_base = k_cumulative_base + (k2 * a_power * b_power)
                k_cumulative_raised = k_cumulative_raised + k3

        print(f"k original: {k}, k cumulative base: {k_cumulative_base}, k cumulative raised: {k_cumulative_raised}")
        print(f"Non-zero codes: {non_zero_codes}")
        print("-------------\n\n")



if __name__ == "__main__":
    print("FACTORIZING CONNECTED POLYNOMIALS\n")
    factorize_connected_polynomials()
    pass