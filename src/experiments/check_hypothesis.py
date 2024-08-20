from src.helpers.polynomials import PolynomialHelper
from src.helpers.parameters import ProposeParameters
from src.core import BBCode
import math


def check_gcd_hypothesis():
    for l in range(10, 1000):
        x_choices = [i for i in range(1, l) if math.gcd(i, l) != 1]
        print(f"l = {l}, x_choices = {x_choices}")
        for x in x_choices:
            x2 = (x ** 2) % l
            if math.gcd(x2, l) == 1:
                print("Hypothesis is wrong.")


def check_equivalence_hypothesis():
    l = 12
    m = 12
    poly_help = PolynomialHelper(l, m)
    propose = ProposeParameters(l, m)

    num_shots = 1000
    for i in range(num_shots):
        A, B = propose.distribute_monomials(propose.draw_random_monomials(3, 3))
        code = BBCode(l, m, A, B)
        n, k, d = code.generate_bb_code(distance_method=3)

        if k == 0:
            continue

        print(f"A: {A}, B: {B}")
        print(f"code: [{n}, {k}, {d}]")

        random_1, random_2 = propose.distribute_monomials(propose.draw_bivariate_monomials(10))
        for m1, m2 in zip(random_1, random_2):
            print(f"m1: {m1}, m2: {m2}")
            A_new = poly_help.multiply_polynomials(A, [m1])
            B_new = poly_help.multiply_polynomials(B, [m2])
            code_new = BBCode(l, m, A_new, B_new)
            n_new, k_new, d_new = code_new.generate_bb_code(distance_method=3)

            if k_new != k or not d / 1.15 < d_new < d * 1.15:
                print("Hypothesis is wrong.")
                print(f"A_new: {A_new}, B_new: {B_new}")
                print(f"code_new: [{n_new}, {k_new}, {d_new}]")
                input("Press <Enter> to continue...")

        print("\n\n")

    pass




if __name__ == "__main__":
    check_equivalence_hypothesis()
    pass









