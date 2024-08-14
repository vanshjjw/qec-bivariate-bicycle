from sage.all import *
import numpy as np

def symmetric_group(*args, **kwargs):
    n = 3

    S3 = SymmetricGroup(Integer(n))
    cayley = S3.cayley_table()
    products = cayley.table()

    G = len(products)
    a = [1,1,0,1,0,0]
    b = [1,0,1,0,0,1]

    A = np.ones(shape=(G,G))
    B = np.ones(shape=(G,G))

    for i in range(G):
        for j in range(G):
            for k in range(G):
                if products[0][i] == products[k][j]:
                    A[i][j] = (A[i][j] + a[k]) % 2

                if products[0][i] == products[j][k]:
                    B[i][j] = (B[i][j] + b[k]) % 2

    return A, B


def cyclic_group():
    pass







