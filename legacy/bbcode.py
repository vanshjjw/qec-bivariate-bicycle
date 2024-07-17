import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import matrix_rank as rank
from numpy.linalg import matrix_power as power
#from numpy.linalg import block_diag
import itertools
import galois
import subprocess
import re


def convert_to_gap_mat(mat):
        """
        Args: 
            mat (np.array): matrix 
        """
        mat = np.array(mat,dtype=int)
        n_rows, n_cols = mat.shape
        mat_str = [','.join(map(str, row)) for row in mat]
        mat_str = '],\n['.join(mat_str)
        gap_code = "M := [".format(n_rows,n_cols) + "[" + mat_str + "]];;\n"
        return gap_code 

def definecode(h):    
    commands='LoadPackage("guava");;'+convert_to_gap_mat(h)+'c:=GeneratorMatCode(M,GF(2));'
    #start_time = time.time()
    process = subprocess.Popen(['gap'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(commands)
    #Remove the special characters from gap's output like colours etc so you can search through it
    #ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    #stdout=ansi_escape.sub('', stdout)
    #stdout=stdout.strip().replace(" ", "")
    print(stdout)
    return stdout

definecode([[1,1,0,0],[0,0,1,1]])

def rank_mod2(A):
    GF2 = galois.GF(2)
    return rank(GF2(np.array(A, dtype=int)))

def binary_combinations(length):
    for bits in itertools.product([0, 1], repeat=length):
        yield list(bits)


def distance(n, HX, HZ):
    H = block_diag(HX, HZ)
    rx=rank_mod2(HX)
    rz=rank_mod2(HZ)
    
    logicals = []
    l1 = binary_combinations(2 * HX.shape[1])
    l2 = np.array([item for item in l1 if np.all(np.matmul(H, item) % 2 == 0)])
    
    for op in l2:
        if rank_mod2(np.vstack((HX, op[:int(n)]))) > rx:
            logicals.append(op)
            continue
        if rank_mod2(np.vstack((HZ, op[int(n):]))) > rz:
            logicals.append(op)
            continue
    
    weights = np.array([np.sum(logical) for logical in logicals])
    d = np.min(weights)

    return d

def code(l,m, a=[3,1,2], b=[3,1,2], c=[1,1,0]):
    """
    A_1=x^a[0], A_2=y^a[1], A_3=y^a[2]
    B_1=y^b[0], B_2=x^b[1], B_3=x^b[2]

    Coefficients c=[1,1,0] for two term polynomials (Toric src),
    c=[1,1,1] for three term polynomials (BB codes)
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

    return(HX, HZ)

def G(H_x, H_z):
    H_x=row_echelon_HS(H_x, full=False)[0]
    H_z=row_echelon_HS(H_z, full=True)[0]
    H_x = H_x[~np.all(H_x == 0, axis=1)]
    H_z = H_z[~np.all(H_z == 0, axis=1)]
    return block_diag(H_x, H_z)

H_x, H_z = code(2,2, a=[3,1,2], b=[3,1,2], c=[1,1,0])

print(row_echelon_HS(H_x, full=True)[0])

def G(H_x, H_z):
    H_x=row_echelon_HS(H_x, full=False)[0]
    H_z=row_echelon_HS(H_z, full=False)[0]
    H_x = H_x[~np.all(H_x == 0, axis=1)]
    H_z = H_z[~np.all(H_z == 0, axis=1)]
    return block_diag(H_x, H_z)

def standard_form(G):
    n, m = G.shape[1] // 2, G.shape[0]
    k = n-m
    
    G1 = G[:, :n]
    G2 = G[:, n:]
    G1_rref, r, G1_transform_rows, G1_transform_cols = reduced_row_echelon(G1)
    G2=(G1_transform_rows@G2@G1_transform_cols)%2
    G = np.hstack((G1_rref,(G1_transform_rows@G2@G1_transform_cols)%2))

    E=G[r:][n+r:]
    E_rref, s, E_transform_rows, E_transform_cols = reduced_row_echelon(E)
    D=(E_transform_rows@G2[r:][:r])%2
    C=(G2[:r][r:]@E_transform_cols)%2

    A=(G1_rref[:r][r:]@E_transform_cols)%2

    G1_rref[:r][r:]=A
    G2[r:][n+r:]=E_rref
    G2[r:][:r]=D
    G2[:r][r:]=C

    G_new=np.hstack((G1_rref, G2))

    return G_new





