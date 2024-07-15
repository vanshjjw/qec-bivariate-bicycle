import numpy as np
from ldpc.mod2 import reduced_row_echelon, rank
from Hasan import standard_form

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
    return rank(A)


def hamming_weight(vector):
    # hamming weight for a CSS code logical operator (length = 2n)
    n = len(vector) // 2
    weight = sum([1 if vector[i] == 1 or vector[i + n] == 1 else 0 for i in range(n)])
    return weight



