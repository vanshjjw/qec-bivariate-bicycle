from sage.all import *
import numpy as np
import re


def convert_string_to_expression(exp: list[str], x, y):
    """
    x, y: generators of the group

    The strings in exp are converted to expressions in x and y.
    """
    expression = []
    for exp in exp:
        # Replace '^' with '**Integer(' and close the parenthesis
        exp = re.sub(r'\^', '**Integer(', exp)
        # Add closing parenthesis for Integer exponents
        exp = re.sub(r'(\*\*Integer\(\-?\d+)', r'\1)', exp)
        # Add Integer for standalone exponents like `y^-1`
        exp = re.sub(r'([xy])(\-?\d+)', r'\1**Integer(\2)', exp)
        expression.append(eval(exp))
    return expression

def make_group(gen: list[str], rel: list[str], a: list[str], b: list[str]):
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


def block_matrix(G, alg, action: str):
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


## ----------------- Inputs ----------------- ##
gen = ['x', 'y'] #list of group generators (two generators for Symmetric groups).
rel = ['x^3', 'y^2', 'x*y^-1*x*y'] #group relators, must use the same generator names defined in gen.

#group algebra elements used to make A and B matrices.
a = ['1','x','x*y']
b = ['1','y','y*x^2']

## ----------------- Parity Check Matrices ----------------- ##
G, a, b = make_group(gen, rel, a, b)

#A always has action == 'left' and B always has action == right
A=block_matrix(G, a, 'left')
B=block_matrix(G, b, 'right')

H_x = np.hstack((A, B))
H_z = np.hstack((B.T, A.T))
print(H_x)





