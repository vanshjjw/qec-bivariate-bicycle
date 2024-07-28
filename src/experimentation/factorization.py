from src.experimentation.parameter import ProposeParameters
from src.core import BBCode
import random
import numpy as np


def multiply_polynomials_mod_2(poly1: list[str], poly2: list[str], l, m):
    result = set()
    for m1 in poly1:
        for m2 in poly2:
            all_combs = m1.split(".") + m2.split(".")
            x_power = sum([int(a[1:]) for a in all_combs if a[0] == "x"])
            y_power = sum([int(h[1:]) for h in all_combs if h[0] == "y"])
            x_power %= l
            y_power %= m
            answer = f"x{x_power}.y{y_power}"

            if answer in result:
                result.remove(answer)
            else:
                result.add(answer)

    return list(result)




def check_product_polynomials():
    l = 9
    m = 9
    num_shots = 100
    propose = ProposeParameters(l = l, m = m)
    print("\n")

    for i in range(num_shots):
        num_x1 = random.randint(2, 3)
        num_y1 = random.randint(2, 3)
        num_x2 = random.randint(2, 3)
        num_y2 = random.randint(2, 3)

        A1, B1 = propose.distribute_monomials(propose.draw_random_monomials(num_x1, num_y1))
        A2, B2 = propose.distribute_monomials(propose.draw_random_monomials(num_x2, num_y2))

        A3 = multiply_polynomials_mod_2(A1, A2, l, m)
        B3 = multiply_polynomials_mod_2(B1, B2, l, m)

        code1 = BBCode(l, m, A1, B1)
        code2 = BBCode(l, m, A2, B2)
        code3 = BBCode(l, m, A3, B3)

        n1, k1, d1 = code1.generate_bb_code(distance_method=3)
        n2, k2, d2 = code2.generate_bb_code(distance_method=3)
        n3, k3, d3 = code3.generate_bb_code(distance_method=3)

        print(f"Trial {i}: l = {l}, m = {m}")
        print(f"Results for code 1: [{n1}, {k1}, {d1}]")
        print(f"Results for code 2: [{n2}, {k2}, {d2}]")
        print(f"Results for code 3: [{n3}, {k3}, {d3}]")
        print("\n")
        print(f"Polynomials 1: {A1}, {B1}")
        print(f"Polynomials 2: {A2}, {B2}")
        print(f"Polynomials 3: {A3}, {B3}")
        print("\n\n")

check_product_polynomials()














