from src.experimentation.propose_parameters import ProposeParameters
from src.core import BBCode
import numpy as np
import src.helpers as helper
import math

def find_min_order(value, l: int, m: int) -> int:
    if value[1] == 0:
        return l // math.gcd(value[0], l)
    if value[0] == 0:
        return m // math.gcd(value[1], m)
    return min(l // math.gcd(value[0], l), m // math.gcd(value[1], m))


def custom_contains(generators: list[(int, int)], value: (int, int), l, m) -> bool:
    order = find_min_order(value, l, m)
    print(f"checking for {value} with order {order} in {generators}")

    for generator in generators:
        for q in range(1, order):
            print(f"q = {q}, value = {value}, check_value = {value[0] ** q % l, value[1] ** q % m}")
            if (value[0] ** q) % l == generator[0] and (value[1] ** q) % m == generator[1]:
                return True
    return False


def generators_for_graph(A: list[str], B: list[str], l: int, m: int, make_independent = True) -> np.ndarray:
    generators : list[str] = []

    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            answer = helper.multiply_m1_and_m2_inverse(A[i], A[j], l, m)
            if not make_independent or not custom_contains(generators, answer, l, m):
                print("True")
                generators.append(answer)

    for i in range(len(B)):
        for j in range(i + 1, len(B)):
            answer = helper.multiply_m1_and_m2_inverse(B[i], B[j], l, m)
            if not make_independent or not custom_contains(generators, answer, l,  m):
                print("True")
                generators.append(answer)

    return helper.construct_expression_from_powers(generators, l, m)



def check():
    l = 16
    m = 16
    num_shots = 1
    p = ProposeParameters(l, m)
    print(f"l = {l}, m = {m}")

    for i in range(num_shots):
        # A, B = p.distribute_monomials(p.draw_random_monomials(3, 3))
        # A = ['x4', 'y3', 'y1']
        # B = ['x10', 'x13', 'y8']

        A = ['i', 'x2', 'x4']
        B = ['i', 'y1', 'y3']

        print(f"A = {A} \nB = {B} \n")

        G = generators_for_graph(A, B, l, m, make_independent=False)
        print(f"G = {G}\n")

        G = generators_for_graph(A, B, l, m, make_independent=True)
        print(f"G = {G}\n")

        print("---------------------------------------------------")


if __name__ == "__main__":
    check()
