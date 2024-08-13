from sage.all import *
import numpy as np

S3 = SymmetricGroup(Integer(3))

cayley=S3.cayley_table()

products=cayley.table()

G=len(products)
a=[1,1,0,1,0,0]
b=[1,0,1,0,0,1]
A=np.ones(shape=(G,G))
B=np.ones(shape=(G,G))
for i in range(G):
    for j in range(G):
        for k in range(G):
            if products[0][i] == products[k][j]:
                A[i][j]=(A[i][j]+a[k])%2
            if products[0][i] == products[j][k]:
                B[i][j]=(B[i][j]+b[k])%2

H_x = np.hstack((A, B))
H_z = np.hstack((B.T, A.T))
# M = H_x @ H_z.T %2
# print(M)







