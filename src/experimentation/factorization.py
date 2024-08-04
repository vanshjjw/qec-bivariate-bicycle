from src.experimentation.propose_parameters import ProposeParameters
from src.polynomials import PolynomialGenerator
from src.core import BBCode
import numpy as np
import src.helpers as helper



def check():
    l = 16
    m = 16
    num_shots = 10
    parameters = ProposeParameters(l, m)
    poly_func = PolynomialGenerator(l, m)


    for i in range(num_shots):
        A, B = parameters.distribute_monomials(parameters.draw_random_monomials(3, 3))
        # A = ['x3', 'y5', 'x5']
        # B = ['y3', 'x5']
        print(f"l = {l}, m = {m}, A: {A}, B: {B}\n")

        H_unique = poly_func.find_graph_generators(A, B, unique=False)
        print(f"Unique generators: {H_unique}\n")

        H_size = poly_func.group_size(H_unique)
        print(f"Size of the group: {H_size}\n")


if __name__ == "__main__":
    check()
