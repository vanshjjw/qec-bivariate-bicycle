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

def generators(A):
    GF2 = galois.GF(2)
    A = GF2(A)
    rref_matrix, pivots = A.rref()
    return rref_matrix[~np.all(rref_matrix == 0, axis=1)]

def hamming_weight(vect):
    weight = sum([1 if vect[i] == 1 or vect[i + len(vect)//2] == 1 else 0 for i in range(len(vect)//2)])


