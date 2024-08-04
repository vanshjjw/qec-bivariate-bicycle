from src.experimentation.propose_parameters import ProposeParameters
from src.core import BBCode
import numpy as np
import src.helpers as helper
import math

def generate_subgroup(value: (int, int), l: int, m: int) -> list[(int, int)]:
    order = find_min_order(value, l, m)
    group = []
    for power in range(1, order):
        my_value = ((value[0] * power) % l, (value[1] * power) % m)
        group.append(my_value)
    return group


def find_min_order(value: (int, int), l: int, m: int) -> int:
    if value[0] == 0:
        return int(math.ceil(m / math.gcd(value[1], m)))
    if value[1] == 0:
        return int(math.ceil(l / math.gcd(value[0], l)))
    return int(math.ceil(l / math.gcd(value[0], l)))


def custom_contains(generators: list[(int, int)], value: (int, int), l, m) -> bool:
    if len(generators) == 0 or value == (0, 0):
        return False

    value_order = find_min_order(value, l, m)

    for generator in generators:
        for power in range(1, value_order):
            if (value[0] * power) % l == generator[0] and (value[1] * power) % m == generator[1]:
                return True

        generator_order = find_min_order(generator, l, m)
        for power in range(1, generator_order):
            if (generator[0] * power) % l == value[0] and (generator[1] * power) % m == value[1]:
                return True

    return False



def remove_duplicate_generators(generators: list[str], l: int, m: int) -> list[str]:
    generator_powers: list[(int, int)] = helper.construct_powers_from_expression(generators, l, m)
    unique: list[(int, int)] = []

    for generator in generator_powers:
        if not custom_contains(unique, generator, l, m):
            unique.append(generator)

    return helper.construct_expression_from_powers(unique, l, m)


def generators_for_graph(A: list[str], B: list[str], l: int, m: int) -> list[str]:
    generators : list[str] = []

    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            answer = helper.multiply_m1_and_m2_inverse(A[i], A[j], l, m)
            generators.append(answer)

    for i in range(len(B)):
        for j in range(i + 1, len(B)):
            answer = helper.multiply_m1_and_m2_inverse(B[i], B[j], l, m)
            generators.append(answer)

    return helper.construct_expression_from_powers(generators, l, m)



def check():
    l = 16
    m = 16
    num_shots = 5
    p = ProposeParameters(l, m)

    for i in range(num_shots):
        # A, B = p.distribute_monomials(p.draw_random_monomials(3, 3))

        A = ['i', 'x2']
        B = ['i', 'y2']

        print(f"l = {l}, m = {m}, A = {A}, B = {B} \n")

        G_all = generators_for_graph(A, B, l, m)
        print(f"All generators G = {G_all}\n")

        G_unique = remove_duplicate_generators(G_all, l, m)
        print(f"Unique generators G = {G_unique}\n")

        G_removed = [x for x in G_all if x not in G_unique]
        print(f"Removed {len(G_removed)} generators = {G_removed}\n\n\n")


if __name__ == "__main__":
    check()
