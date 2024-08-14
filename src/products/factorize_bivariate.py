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
    l = 14
    m = 14
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
    code_cached = BBCodeCached(l, m)

    num_shots = 500


    for i in range(10):
        if i % 500 == 0:
            print(f"{i}/{num_shots} completed.\n")
            parameters, poly_help, code_cached = change_parameters()

        # Factorize Toric Polynomials
        # A = i + x + x^{a}.y^{b}
        # B = i + y + x^{c}.y^{d}

        bivariates = parameters.draw_bivariate_monomials(2)
        A = ["i", "x"] + bivariates[0]
        B = ["i", "y"] + bivariates[1]

        n, k, d = code_cached.set_expressions(A, B).generate_bb_code(distance_method=4)






if __name__ == "__main__":
    factorize_bivariate_polynomials()
    pass