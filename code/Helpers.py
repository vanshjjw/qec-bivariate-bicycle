import numpy as np
import galois

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


def create_matrix_S(size):
    S = np.eye(size, dtype=int, k = 1)
    S[size - 1][0] = 1
    return S


def calculate_rank_GF2(A):
    GF = galois.GF(2)
    rank = np.linalg.matrix_rank(GF(A))
    return rank

