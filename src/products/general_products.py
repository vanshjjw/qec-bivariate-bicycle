from src.propose_parameters import ProposeParameters
from src.polynomials import PolynomialHelper
from src.core import BBCode
import src.helpers as helper
import random


def multiply_random_polynomials():
    # multiply two random polynomials and check if the resulting code has a larger k value
    # conclusion: the k value of the product polynomial is always >= k of original polynomials
    l = 9
    m = 9
    num_shots = 1
    propose = ProposeParameters(l = l, m = m)
    poly_help = PolynomialHelper(l, m)
    print("\n")

    for i in range(num_shots):
        min_num = 2
        max_num = 4

        num_x1 = random.randint(min_num, max_num)
        num_y1 = random.randint(min_num, max_num)
        num_x2 = random.randint(min_num, max_num)
        num_y2 = random.randint(min_num, max_num)

        # base code
        A1, B1 = propose.distribute_monomials(propose.draw_random_monomials(num_x1, num_y1))
        A2, B2 = propose.distribute_monomials(propose.draw_random_monomials(num_x2, num_y2))

        code1 = BBCode(l, m, A1, B1)
        code2 = BBCode(l, m, A2, B2)

        n1, k1, d1 = code1.generate_bb_code(distance_method=0)
        n2, k2, d2 = code2.generate_bb_code(distance_method=0)

        # unnecessary cases
        if k1 == 0 and k2 == 0:
            continue

        A3 = poly_help.multiply_polynomials(A1, A2)
        B3 = poly_help.multiply_polynomials(B1, B2)

        code3 = BBCode(l, m, A3, B3)

        n3, k3, d3 = code3.generate_bb_code(distance_method=0)

        if k3 >= k2 or k3 >= k1:
            print(f"Trial {i}: l = {l}, m = {m}")
            print(f"Results for code 1: [{n1}, {k1}, {d1}]")
            print(f"Results for code 2: [{n2}, {k2}, {d2}]")
            print(f"Results for code 3: [{n3}, {k3}, {d3}]")
            print("\n")
            print(f"Polynomials 1: {A1}, {B1}")
            print(f"Polynomials 2: {A2}, {B2}")
            print(f"Polynomials 3: {A3}, {B3}")
            print("\n\n")

        if i % 1000 == 0:
            print(f"Trial {i} completed.")
            l = random.randint(8, 14)
            m = random.randint(8, 14)

        pass


def square_polynomials():
    # square a polynomial and check if the resulting code has a larger k value
    # conclusion: the k value increases by the same factor as the number of connected components
    l = 32
    m = 32
    poly_help = PolynomialHelper(l, m)
    A = ["i", "x"]
    B = ["i", "y"]

    for i in range(1, 10):
        code = BBCode(l, m, A, B, safe_mode=False)
        n, k, d = code.generate_bb_code(distance_method=0)
        num_components = helper.num_connected_components(code.graph())

        print(f"A : {A}: \nB: {B} \n")
        print(f"code: [{n}, {k}, {d}]")
        print(f"Number of components: {num_components}")
        print("\n\n")

        A = poly_help.multiply_polynomials(A, A)
        B = poly_help.multiply_polynomials(B, B)



if __name__ == "__main__":
    square_polynomials()
    pass













