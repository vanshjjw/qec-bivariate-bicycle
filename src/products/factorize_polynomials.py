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


# Factorize the disconnected polynomials to break down the code into connected components.
def factorize_disconnected_polynomials():
    l = 16
    m = 16
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
    num_shots = 1000

    for i in range(num_shots):
        if i % 50 == 0:
            print(f"{i}/{num_shots} completed.")

        A = parameters.draw_random_monomials(3, 0)
        B = parameters.draw_random_monomials(0, 3)

        code = BBCode(l, m, A, B)
        n, k, d = code.generate_bb_code(distance_method=3)

        if k == 0:
            continue

        graph = code.graph()
        num_components = helper.num_connected_components(graph)
        is_connected = helper.is_connected(graph)

        if is_connected:
            continue

        factors_of_A = poly_help.factorize(A, is_x=True)
        factors_of_B = poly_help.factorize(B, is_x=False)

        print(f"Original polynomials. A : {A}, B : {B}")
        print(f"Original code: [{n}, {k}, {d}]")
        print(f"Number of components in original graph: {num_components}")
        print(f"Factorization of A: {factors_as_strings(factors_of_A)}")
        print(f"Factorization of B: {factors_as_strings(factors_of_B)}")
        print("\n")


        for fa in factors_of_A[0]:
            for fb in factors_of_B[0]:
                print(f"new polynomials: A : {fa}, B : {fb}")
                code = BBCode(l, m, fa, fb)
                n, k, d = code.generate_bb_code(distance_method=3)
                print(f"New code: [{n}, {k}, {d}]")
                graph = code.graph()
                if helper.is_connected(graph):
                    print("New graph is connected.")
                else:
                    print(f"Number of components in new graph: {helper.num_connected_components(graph)}")
                print("\n")

        print("-------------\n\n")
    pass




if __name__ == "__main__":
    factorize_disconnected_polynomials()
    pass