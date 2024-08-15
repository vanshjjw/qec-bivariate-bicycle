#%%
from sage.all import *
import numpy as np
import re

def convert_string_to_expression(rel,x,y):
    expression = []
    if '+' in rel:
        list=rel.strip().split('+')
    else:
        list=rel
    for exp in list:
        # Replace '^' with '**Integer(' and close the parenthesis
        exp = re.sub(r'\^', '**Integer(', exp)
        # Add closing parenthesis for Integer exponents
        exp = re.sub(r'(\*\*Integer\(\-?\d+)', r'\1)', exp)
        # Add Integer for standalone exponents like `y^-1`
        exp = re.sub(r'([xy])(\-?\d+)', r'\1**Integer(\2)', exp)
        expression.append(eval(exp))
    return expression

def make_group(gen, rel, a, b):
    F = FreeGroup(gen)
    x, y = F._first_ngens(2)
    rel = convert_string_to_expression(rel,x,y)
    G = F / rel
    x,y=G.gens()
    a = convert_string_to_expression(a, x, y)
    b = convert_string_to_expression(b, x, y)
    for i in range(len(a)):
        if a[i] == 1:
            a[i] = G.list()[0]
    for i in range(len(b)):
        if b[i] == 1:
            b[i] = G.list()[0]

    return G, a, b


def block_matrix(G, alg, action):
    elms=G.list()
    m=len(elms)
    M=np.ones(shape=(m,m))

    if action == 'left':
        for alg_elm in alg:
            for i in range(m):
                for j in range(m):
                    if elms[i] == alg_elm*elms[j]:
                        M[i][j]=(M[i][j]+1)%2
    else:
        for alg_elm in alg:
            for i in range(m):
                for j in range(m):
                    if elms[i] == elms[j]*alg_elm:
                        M[i][j]=(M[i][j]+1)%2

    return M

gen = ['x', 'y']
rel = ['x^3', 'y^2', 'x*y^-1*x*y']
a = '1+x+x*y'
b = '1+y+y*x^2'

G, a, b = make_group(gen, rel, a, b)

A=block_matrix(G, a, 'left')
B=block_matrix(G, b, 'right')

H_x = np.hstack((A, B))
H_z = np.hstack((B.T, A.T))
M = H_x @ H_z.T %2
print(M)





#%%

# S3 = SymmetricGroup(Integer(3))
#
# cayley=S3.cayley_table()
#
# products=cayley.table()
#
# G=len(products)
# a=[1,1,0,1,0,0]
# b=[1,0,1,0,0,1]
# A=np.ones(shape=(G,G))
# B=np.ones(shape=(G,G))
# for i in range(G):
#     for j in range(G):
#         for k in range(G):
#             if products[0][i] == products[k][j]:
#                 A[i][j]=(A[i][j]+a[k])%2
#             if products[0][i] == products[j][k]:
#                 B[i][j]=(B[i][j]+b[k])%2
#
# H_x = np.hstack((A, B))
# H_z = np.hstack((B.T, A.T))
# M = H_x @ H_z.T %2
# print(M)







