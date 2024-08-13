from src.polynomial_helper import PolynomialHelper
from src.propose_parameters import ProposeParameters
from src.core_cached import BBCodeCached


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


    for i in range(10):
        A, B = parameters.distribute_monomials(parameters.draw_random_monomials(3, 3))
        C = parameters.draw_bivariate_monomials(4)

        A_Factors = poly_help.factorize_bivariate(A)
        B_Factors = poly_help.factorize_bivariate(B)
        C_Factors = poly_help.factorize_bivariate(C)

        print("Original polynomials.")
        print(f"A : {A}")
        print(f"B : {B}")
        print(f"C : {C}")
        print("\n")
        print("Factorized polynomials.")
        print(f"A : {factors_as_strings(A_Factors)}")
        print(f"B : {factors_as_strings(B_Factors)}")
        print(f"C : {factors_as_strings(C_Factors)}")
        print("\n\n")




if __name__ == "__main__":
    factorize_bivariate_polynomials()
    pass