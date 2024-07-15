import numpy as np
import galois
from copy import deepcopy
from ldpc.mod2 import reduced_row_echelon, inverse
from utils_linalg import *
from scipy.linalg import block_diag

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

def compute_standard_form(G):
    """
    Returns the standard form of a stabilizer code. 
    See Nielsen & Chuang Section 10.5.7.
    """
    n, m = G.shape[1] // 2, G.shape[0]
    k = n-m
    
    G1 = G[:, :n]
    G2 = G[:, n:]

    ## LOGICALS

    # Step 1: Gaussian Elimination on G1 & adjust G2 rows & cols accordingly
    G1_rref, r, G1_transform_rows, G1_transform_cols = reduced_row_echelon(G1)
    G = np.hstack((G1_rref,(G1_transform_rows@G2@G1_transform_cols)%2))

    # Step 2: Swap columns r to n from X to Z block 
    G[:,r:n], G[:,n+r:2*n] = G[:,n+r:2*n].copy(), G[:,r:n].copy()
    E1 = G[:, :n]
    E2 = G[:, n:]
    E1_rref, e, E_transform_rows, E_transform_cols = reduced_row_echelon(E1)
    s = e - r
    G = np.hstack((E1_rref,(E_transform_rows@E2@E_transform_cols)%2))
    G[:,r:n], G[:,n+r:2*n] = G[:,n+r:2*n].copy(), G[:,r:n].copy()

    # Step 3: Z Logicals
    A_2 = G[:r,n-k:n]
    C = G[:r,(2*n-k):]
    E = G[r:,(2*n-k):]

    r1 = A_2.T
    r2 = np.zeros((k,n-k-r))
    r3 = np.eye(k)
    right = np.hstack((np.hstack((r1,r2)),r3))
    Z_logicals = np.hstack((np.zeros((k,n)),right))
    Z_logicals = np.array(Z_logicals,dtype=int)
    for z in Z_logicals:
        assert len(z) == 2*n
        assert np.allclose(symplectic_prod_mat_vec(G,z),np.zeros((G.shape[0])))

    # Step 4: X Logicals
    l1 = np.zeros((k,r))
    l2 = E.T
    l3 = np.eye(k)
    left = np.hstack((np.hstack((l1,l2)),l3))
    r1 = C.T
    r2 = np.zeros((k,n-k-r))
    r3 = np.zeros((k,k))
    right = np.hstack((np.hstack((r1,r2)),r3))
    X_logicals = np.hstack((left,right))
    X_logicals = np.array(X_logicals,dtype=int)
    for x in X_logicals:
        assert len(x) == 2*n
        assert np.allclose(symplectic_prod_mat_vec(G,x),np.zeros((G.shape[0])))

    # Step 5: Move columns (but not rows) back to their original position
    inv_E_transform_cols = inverse(E_transform_cols)
    inv_G1_transform_cols = inverse(G1_transform_cols)
    inv_transform_cols = inv_E_transform_cols @ inv_G1_transform_cols
    ## STABILIZERS
    G_new = np.zeros_like(G)
    G_new[:,:n] = (G[:,:n] @ inv_transform_cols)%2
    G_new[:,n:] = (G[:,n:] @ inv_transform_cols)%2
    ## LOGICALS
    Z_logicals_og_basis = np.zeros_like(Z_logicals)
    X_logicals_og_basis = np.zeros_like(X_logicals)
    Z_logicals_og_basis[:,:n] =  (Z_logicals[:,:n] @ inv_transform_cols)%2
    Z_logicals_og_basis[:,n:] =  (Z_logicals[:,n:] @ inv_transform_cols)%2
    X_logicals_og_basis[:,:n] =  (X_logicals[:,:n] @ inv_transform_cols)%2
    X_logicals_og_basis[:,n:] =  (X_logicals[:,n:] @ inv_transform_cols)%2
    """ ## DESTABILIZERS 
    DX = np.hstack([np.zeros((r,n)),np.eye(r),np.zeros((r,n-r))])
    DZ = np.hstack([np.zeros((s,r)),np.eye(s),np.zeros((s,n+k))])
    D = np.array(np.vstack([DX,DZ]),dtype=int)
    D_og_basis = np.zeros_like(D)
    D_og_basis[:,:n] =  (D[:,:n] @ inv_transform_cols)%2
    D_og_basis[:,n:] =  (D[:,n:] @ inv_transform_cols)%2 """

    return G_new, X_logicals_og_basis, Z_logicals_og_basis#, D_og_basis

def symplectic_inner_prod(vec1, vec2):

    if len(vec1) != len(vec2):

        raise ValueError("Vectors must be of the same length")

    if len(vec1) % 2 != 0:

        raise ValueError("Vectors must be of even length")

 

    n = len(vec1) // 2

 

    # Split the vectors into halves

    vec1_first_half = vec1[:n]

    vec1_second_half = vec1[n:]

    vec2_first_half = vec2[:n]

    vec2_second_half = vec2[n:]

 

    # Calculate dot products

    dot_product_first_halves = sum(a * b for a, b in zip(vec1_first_half, vec2_second_half))%2

    dot_product_second_halves = sum(a * b for a, b in zip(vec1_second_half, vec2_first_half))%2

 

    # Compute symplectic inner product

    symplectic_inner_product = (dot_product_first_halves + dot_product_second_halves)%2

 

    return symplectic_inner_product

 

def symplectic_prod_mat_vec(mat,vec):

    # Check if vec2 length is even

    if len(vec) % 2 != 0:

        raise ValueError("Vectors must be of even length")

 

    # Check if all rows in the matrix have the same length as vec2

    row_length = len(vec)

    for row in mat:

        if len(row) != row_length:

            raise ValueError("All rows in the mat must have the same length as vec.")

 

    result = [symplectic_inner_prod(row, vec) for row in mat]

 

    return result

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



def G(H_x, H_z):
    H_x=row_echelon_HS(H_x, full=False)[0]
    H_z=row_echelon_HS(H_z, full=False)[0]
    H_x = H_x[~np.all(H_x == 0, axis=1)]
    H_z = H_z[~np.all(H_z == 0, axis=1)]
    return block_diag(H_x, H_z)