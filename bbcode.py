import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import matrix_rank as rank
from numpy.linalg import matrix_power as power
from scipy.linalg import block_diag
import itertools

def rank_mod2(A):
    if np.count_nonzero(A) == 0:
        return A

    m, n = A.shape
    row = 0

    for col in range(n):
        if A[row:, col].max() == 0:
            continue
        
        max_index = np.argmax(np.abs(A[row:, col])) + row
        A[[row, max_index]] = A[[max_index, row]]


        for r in range(row + 1, m):
            A[r] = (A[r] - A[r, col] * A[row]) % 2

  
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

def distance(n, HX, HZ):
    H = block_diag(HX, HZ)
    hx = np.hstack((HX, np.zeros((n // 2, n))))
    hz = np.hstack((np.zeros((n // 2, n)), HZ))
    
    logicals = []
    l1 = [list(bits) for bits in itertools.product([0, 1], repeat=2 * HX.shape[1])]
    l2 = [item for item in l1 if np.all(np.matmul(H, item) % 2 == 0)]
    
    for op in l2:
        op = np.array(op)
        if rank_mod2(np.vstack((hx, op))) <= rank_mod2(hx):
            continue
        if rank_mod2(np.vstack((hz, op))) <= rank_mod2(hz):
            continue
        if rank_mod2(np.vstack((H, op))) > rank_mod2(H):
            logicals.append(op)
    
    x = np.array([np.sum(logical) for logical in logicals])
    d = np.min(x)

    return d

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
    k=n-rank_mod2(HX)-rank_mod2(HZ)
    d=distance(n,HX,HZ) 

    return(n,k,d)

nt,kt,dt=code(3,3,a=[0,1,0],b=[0,1,0],c=[1,1,0])

print("n=%s" %nt)
print("k=%s" %kt)
print("d=%s" %dt)