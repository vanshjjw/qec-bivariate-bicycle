from src.polynomial_helper import PolynomialHelper
from src.propose_parameters import ProposeParameters
from src.core_cached import BBCodeCached
import random


def change_parameters():
    l, m = random.randint(10, 20), random.randint(10, 20)
    print(f"New parameters: l = {l}, m = {m}\n")
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
    code_cached = BBCodeCached(l, m)
    return parameters, poly_help, code_cached



def factors_as_strings(factors):
    i = 0
    s = ""
    for f, exp in zip(factors[0], factors[1]):
        s += f"{f}^{exp}"
        if i < len(factors[0]) - 1:
            s += "  *  "
        i += 1
    return s


def factorize_bivariate_polynomials():
    l = 12
    m = 12
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
    code_cached = BBCodeCached(l, m)

    num_shots = 10000

    for i in range(num_shots):
        if i % 100 == 0:
            print(f"{i}/{num_shots} completed.")
            print("\n")
        if i % 200 == 0 and i != 0:
            parameters, poly_help, code_cached = change_parameters()

        # Factorize Toric Polynomials
        # A = i + x + x^{a}.y^{b}
        # B = i + y + x^{c}.y^{d}

        bivariates = parameters.draw_bivariate_monomials(2)
        A = ["i", "x", bivariates[0]]
        B = ["i", "y", bivariates[1]]

        n, k, d = code_cached.set_expressions(A, B).generate_bb_code(distance_method=3)
        num_components = code_cached.make_graph().num_connected_components()

        if k == 0:
            continue

        print(f"A : {A}, B : {B}")
        print(f"Code: [{n}, {k}, {d}]\n")
        print(f"Number of connected components: {num_components}\n")

        A_Factors = poly_help.factorize_bivariate(A)
        B_Factors = poly_help.factorize_bivariate(B)

        if len(A_Factors[0]) == 1 and len(B_Factors[0]) == 1 and A_Factors[1][0] == 1 and B_Factors[1][0] == 1:
            print("No factorization possible.")
            print("----------------\n\n")
            continue

        print(f"Factorization of A: {factors_as_strings(A_Factors)}")
        print(f"Factorization of B: {factors_as_strings(B_Factors)}")
        print("\n")

        non_zero_factor_codes = 0

        for i, a in enumerate(A_Factors[0]):
            for j, b in enumerate(B_Factors[0]):

                n2, k2, d2 = code = code_cached.set_expressions(a, b).generate_bb_code(distance_method=3)
                num_components = code_cached.make_graph().num_connected_components()
                print(f"checking factors a{i} and b{j}: code [{n2}, {k2}, {d2}]: has {num_components} components.")

                if k2 == 0:
                    continue
                non_zero_factor_codes += 1

                a_power = A_Factors[1][i]
                b_power = B_Factors[1][j]

                if a_power == 1 and b_power == 1:
                    continue

                a_raised = poly_help.raise_polynomial_to_power(a, a_power)
                b_raised = poly_help.raise_polynomial_to_power(b, b_power)

                n3, k3, d3 = code_cached.set_expressions(a_raised, b_raised).generate_bb_code(distance_method=4)
                num_components = code_cached.make_graph().num_connected_components()
                print(f"checking factors a{i}^{a_power} and b{j}^{b_power}: code [{n3}, {k3}, {d3}]: "
                      f"has {num_components} components.")

        print("\n")
        print(f"Non-zero factor codes: {non_zero_factor_codes}")
        print("----------------\n\n")



if __name__ == "__main__":
    factorize_bivariate_polynomials()
    pass