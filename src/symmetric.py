from sage.all import *
import numpy as np
import re


def convert_string_to_expression(exp: list[str], gens):
    """
    gens: generators of the group with respect to which the string expression is being evaluated.
    """
    #finding unique alphabetical characters in exp
    unique_chars = set()
    for s in exp:
        unique_chars.update(c for c in s if c.isalpha())
    unique_chars = sorted(unique_chars)

    #naming each generator after one of the unique characters
    variables = {}
    for i in range(len(unique_chars)):
        variables[unique_chars[i]] = gens[i]
    variables['Integer'] = Integer

    expression = []
    for string in exp:
        # Replace '^' with '**Integer(' and close the parenthesis
        string = re.sub(r'\^', '**Integer(', string)
        # Add closing parenthesis for Integer exponents
        string = re.sub(r'(\*\*Integer\(\-?\d+)', r'\1)', string)
        # Add Integer for standalone exponents like `y^-1`
        string = re.sub(r'([a-zA-Z])(\-?\d+)', r'\1**Integer(\2)', string)
        expression.append(eval(string, {}, variables))
    return expression

# gen = ['r']
# rel = ['r^10']
#
# F = FreeGroup(gen)
# fgens = F._first_ngens(len(gen))
# rel = convert_string_to_expression(rel,fgens)
# G = F/rel
# gens = G.gens()
# print(G.list()[1]**10 == G.list()[0])

# def convert_string_to_expression(exp: list[str], x, y):
#     """
#     x, y: generators of the group
#
#     The strings in exp are converted to expressions in x and y.
#     """
#     expression = []
#     for string in exp:
#         # Replace '^' with '**Integer(' and close the parenthesis
#         string = re.sub(r'\^', '**Integer(', string)
#         # Add closing parenthesis for Integer exponents
#         string = re.sub(r'(\*\*Integer\(\-?\d+)', r'\1)', string)
#         # Add Integer for standalone exponents like `y^-1`
#         string = re.sub(r'([xy])(\-?\d+)', r'\1**Integer(\2)', string)
#         expression.append(eval(string))
#     return expression

def make_group(gen: list[str], rel: list[str], a: list[str], b: list[str]):
    F = FreeGroup(gen)
    fgens = F._first_ngens(len(gen))
    rel = convert_string_to_expression(rel,fgens)
    G = F / rel
    gens=G.gens()
    a = convert_string_to_expression(a, gens)
    b = convert_string_to_expression(b, gens)
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

# gen = ['x','y'] #list of group generators (two generators for Symmetric groups).
# rel = ['x^9', 'y^4', 'y^-1*x*y*x']
# a = ['1','x','y','y*x^6']
# b = ['1','y^2*x','y^2*x^6','x^2']
## ----------------- Parity Check Matrices ----------------- ##
G, a, b = make_group(gen, rel, a, b)

#A always has action == 'left' and B always has action == right
A=block_matrix(G, a, 'left')
B=block_matrix(G, b, 'right')

H_x = np.hstack((A, B))
H_z = np.hstack((B.T, A.T))
print(H_x@H_z.T %2)




