from src.experimentation.propose_parameters import ProposeParameters
from src.core import BBCode
import numpy as np
import src.helpers as helper
import math


def is_whole_group_generated(generators: list[(int, int)], l: int, m: int) -> bool:
    if type(generators[0]) is str:
        generators = helper.construct_powers_from_expression(generators, l, m)

    x_indices = []
    y_indices = []

    for i, value in enumerate(generators):
        if math.gcd(value[0], l) == 1:
            x_indices.append(i)
            if y_indices is not None:
                # Found a new x generator and a y generator already exists
                return True

        if math.gcd(value[1], m) == 1:
            y_indices.append(i)
            if x_indices is not None and i not in x_indices:
                # Found a new y generator and a different x generator already exists
                return True

    return False






def find_subgroup_size(generators: list[str], l: int, m: int) -> int:
    pass


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
    if len(generators) == 0:
        return False
    if value == (0, 0):
        return True

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


def remove_duplicate_generators(generators: list[(int, int)], l: int, m: int) -> list[str]:
    unique: list[(int, int)] = []

    for generator in generators:
        if not custom_contains(unique, generator, l, m):
            unique.append(generator)

    return helper.construct_expression_from_powers(unique, l, m)


def find_generators(A: list[str], B: list[str], l: int, m: int, unique = True) -> list[str]:
    generators : list[str] = []

    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            answer = helper.multiply_m1_and_m2_inverse(A[i], A[j], l, m)
            generators.append(answer)

    for i in range(len(B)):
        for j in range(i + 1, len(B)):
            answer = helper.multiply_m1_and_m2_inverse(B[i], B[j], l, m)
            generators.append(answer)

    if unique:
        return remove_duplicate_generators(generators, l, m)
    else:
        return helper.construct_expression_from_powers(generators, l, m)



def check():
    l = 15
    m = 15
    num_shots = 5
    p = ProposeParameters(l, m)

    for i in range(num_shots):
        A, B = p.distribute_monomials(p.draw_random_monomials(3, 3))

        A = ['x3', 'y5']
        B = ['y3', 'x5']
        print(f"A: {A}, B: {B}\n")

        H_unique = find_generators(A, B, l, m, unique=True)
        print(f"Unique generators: {H_unique}")

        is_whole_group = is_whole_group_generated(H_unique, l, m)
        print(f"Whole group generated: {is_whole_group}\n\n")


if __name__ == "__main__":
    check()
