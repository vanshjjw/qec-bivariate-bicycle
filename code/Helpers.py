import numpy as np
import galois
from copy import deepcopy


def display(M, middle_line = False):
    size = len(M[0])

    h_line = "--" * size
    print(h_line)

    for row in M:
        print("[ ", end = "")
        for i in range(size):
            print(row[i], end = " ")
            if middle_line and i == size / 2:
                print("|", end = " ")
        print("]")

    print(h_line)
    pass


def calculate_rank_GF2(A):
    GF = galois.GF(2)
    rank = np.linalg.matrix_rank(GF(A))
    return rank


def find_reduced_row_echelon_form(Hx, Hz):
    # return rref form of Hx and Hz
    pass



def find_logical_generators(Sx, Sz):
    # return logical generators of the code
    pass


