import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import matrix_rank as rank
from numpy.linalg import matrix_power as power

def rank_mod2(A):
    # Step 1
    if np.count_nonzero(A) == 0:
        return A

    m, n = A.shape
    row = 0

    for col in range(n):
        # Step 2
        if A[row:, col].max() == 0:
            continue
        
        # Step 3
        max_index = np.argmax(np.abs(A[row:, col])) + row
        A[[row, max_index]] = A[[max_index, row]]

        # Step 4
        for r in range(row + 1, m):
            A[r] = (A[r] - A[r, col] * A[row]) % 2

        # Step 5
        row += 1
        if row >= m:
            break

        ref = A%2
        m, n = ref.shape
        rank = 0
    
        for i in range(m):
            if np.count_nonzero(ref[i, :]) > 0:
                rank += 1
            
    return rank


def code(l,m, a=[3,1,2], b=[3,1,2], c=[1,1,0]):
    """
    A_1=x^a[0], A_2=y^a[1], A_3=y^a[2]
    B_1=y^b[0], B_2=x^b[1], B_3=x^b[2]

    Coefficients c=[1,1,0] for Toric code (two term polynomials),
    c=[1,1,1] for three term polynomials
    """
    Sl = np.zeros(shape=(l,l),dtype=float)
    Sm = np.zeros(shape=(m,m),dtype=float)
    for i in range(l):
        Sl[i][(i+1)%l]=1
    for i in range(m):
        Sm[i][(i+1)%m]=1
    
    I=np.eye(l*m)
    x=np.kron(Sl,np.eye(m))
    y=np.kron(np.eye(l),Sm)
    
    A=(c[0]*power(x,a[0])%2 + c[1]*power(y,a[1])%2 + c[2]*power(y,a[2])%2)%2
    B=(c[0]*power(y,b[0])%2 + c[1]*power(x,b[1])%2 + c[2]*power(x,b[2])%2)%2

    HX=np.hstack((A,B))
    HZ=np.hstack((B.transpose(),A.transpose()))

    n=2*l*m
    k=n-rank_mod2(HX)-rank_mod2(HZ) #seems to work for even-even l,m only (probably need to do rank over F_2 ^(n/2 x n))

    return(n,k)

nt,kt=code(8,5,a=[0,1,0],b=[0,1,0],c=[1,1,0])

print("n=%s" %nt)
print("k=%s" %kt)
