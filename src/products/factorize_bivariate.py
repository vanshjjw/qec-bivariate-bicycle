from src.polynomial_helper import PolynomialHelper
from src.propose_parameters import ProposeParameters
from src.core_cached import BBCodeCached


def factorize_bivariate_polynomials():
    l = 14
    m = 14
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)
    code_cached = BBCodeCached(l, m)

    A = parameters.draw_random_monomials(1,2)
    B = parameters.draw_random_monomials(2,1)

    n, k, d = code_cached.set_expressions(A, B).generate_bb_code(distance_method=4)

    A_Factors = poly_help.factorize_bivariate(A)
    B_Factors = poly_help.factorize_bivariate(B)

    print(f"Original polynomials. A : {A}, B : {B}")
    print(f"Original code: [{n}, {k}, {d}]")
    print(f"Factorization of A: {A_Factors}")
    print(f"Factorization of B: {B_Factors}")




if __name__ == "__main__":
    factorize_bivariate_polynomials()
    pass