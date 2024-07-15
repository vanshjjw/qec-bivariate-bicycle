import numpy as np
from ldpc.mod2 import reduced_row_echelon, rank
from scipy.linalg import block_diag
from Hasan.utils_linalg import row_echelon_HS

def standard_form(G):
    n, m = G.shape[1] // 2, G.shape[0]
    k = n-m

    G1 = G[:, :n]
    G2 = G[:, n:]
    G1_rref, r, G1_transform_rows, G1_transform_cols = reduced_row_echelon(G1)
    G2=(G1_transform_rows@G2@G1_transform_cols)%2
    G = np.hstack((G1_rref,G2))

    E=G2[r:,r:]
    E_rref, s, E_transform_rows, E_transform_cols = reduced_row_echelon(E)
    D=(E_transform_rows@G2[r:,:r])%2
    C=(G2[:r,r:]@E_transform_cols)%2

    A=(G1_rref[:r,r:]@E_transform_cols)%2

    G1_rref[:r,r:]=A
    G2[r:,r:]=E_rref
    G2[r:,:r]=D
    G2[:r,r:]=C

    G_new=np.hstack((G1_rref, G2))

    return G_new


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



def pre_process(H_x, H_z):
    H_x=row_echelon_HS(H_x, full=False)[0]
    H_z=row_echelon_HS(H_z, full=False)[0]
    H_x = H_x[~np.all(H_x == 0, axis=1)]
    H_z = H_z[~np.all(H_z == 0, axis=1)]
    return block_diag(H_x, H_z)