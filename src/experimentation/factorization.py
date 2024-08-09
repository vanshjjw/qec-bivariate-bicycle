from src.polynomials import PolynomialHelper, PolynomialToGraphs
from src.experimentation.propose_parameters import ProposeParameters
from src.core import BBCode
import src.helpers as helper


def factorize():
    l = 14
    m = 14
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
    num_shots = 1000

    for i in range(num_shots):
        if i % 20 == 0:
            print(f"{i}/{num_shots} completed.")

        A = parameters.draw_random_monomials(3, 0)
        B = parameters.draw_random_monomials(0, 3)

        code = BBCode(l, m, A, B)
        n, k, d = code.generate_bb_code(distance_method=3)

        if k == 0:
            continue

        factors_of_A = poly_help.factorize(A, is_x=True)
        factors_of_B = poly_help.factorize(B, is_x=False)

        if len(factors_of_A) != len(factors_of_B):
            print("Unequal number of factors.")
            continue

        print(f"Original polynomials. A : {A}, B : {B}")
        print(f"code: [{n}, {k}, {d}] \n")

        for factor_A, factor_B in zip(factors_of_A, factors_of_B):
            code_new = BBCode(l, m, factor_A, factor_B)
            n_new, k_new, d_new = code_new.generate_bb_code(distance_method=3)
            print(f"Factors. A : {factor_A}, B : {factor_B}")
            print(f"sub-code: [{n_new}, {k_new}, {d_new}] \n")

        print("\n\n")













if __name__ == "__main__":
    factorize()
    pass