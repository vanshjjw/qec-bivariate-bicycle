from src.experimentation.propose_parameters import ProposeParameters
from src.polynomials import PolynomialHelper
from src.core import BBCode
import src.helpers as helper
import random


def check_product_polynomials():
    l = 9
    m = 9
    num_shots = 1000
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


def check_polynomial_powers():
    l = 12
    m = 12
    poly_help = PolynomialHelper(l, m)
    A = ["x3", "y2", "y7"]
    B = ["y3", "x1", "x2"]

    for i in range(1, 5):
        code = BBCode(l, m, A, B, safe_mode=False)
        n, k, d = code.generate_bb_code(distance_method=3)
        print(f"A : {A}: \nB: {B} \n")
        print(f"Results: [{n}, {k}, {d}]")
        print("\n\n")

        A = poly_help.multiply_polynomials(A, A)
        B = poly_help.multiply_polynomials(B, B)

def product():
    l = 6
    m = 6
    poly_help = PolynomialHelper(l, m)

    A1 = ["x3", "y1", "y2"]
    B1 = ["y3", "x1", "x2"]
    code1 = BBCode(l, m, A1, B1, safe_mode=False)
    G1=code1.graph()
    sub_graphs_1 = helper.compute_sub_graphs(G1)
    print(f"Sub Graphs code 1: {len(sub_graphs_1)}")

    A2 = ["x3", "y2", "y5"]
    B2 = ["y3", "x2", "x5"]
    code2 = BBCode(l, m, A2, B2, safe_mode=False)
    G2 = code2.graph()
    sub_graphs_2 = helper.compute_sub_graphs(G2)
    print(f"Sub Graphs code 2: {len(sub_graphs_2)}")

    A3 = poly_help.multiply_polynomials(A1, A2)
    B3 = poly_help.multiply_polynomials(B1, B2)

    code3 = BBCode(l, m, A3, B3, safe_mode=False)
    G3 = code3.graph()
    sub_graphs_3 = helper.compute_sub_graphs(G3)
    print(f"Sub Graphs: {len(sub_graphs_3)}")




if __name__ == "__main__":
    product()













