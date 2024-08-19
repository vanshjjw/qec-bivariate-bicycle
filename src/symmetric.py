from sage.all import FreeGroup, Integer
import numpy as np
import re
import helpers
import src.distances.distance_from_gap as qdistrand
import src.distances.distance_from_bposd as bposd
import os


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


def make_group(generators: list[str], rel: list[str], a: list[str], b: list[str]):
    F = FreeGroup(generators)
    F_generators = F._first_ngens(len(generators))
    relators = convert_string_to_expression(rel, F_generators)
    G = F / relators
    G_generators = G.gens()
    identity = G_generators[0]**Integer(0)
    a = convert_string_to_expression(a, G_generators)
    b = convert_string_to_expression(b, G_generators)

    for i in range(len(a)):
        if a[i] == 1:
            a[i] = identity
    for i in range(len(b)):
        if b[i] == 1:
            b[i] = identity

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
                        M[i][j] = (M[i][j]+1)%2
    else:
        for alg_elm in alg:
            for i in range(m):
                for j in range(m):
                    if elms[i] == elms[j]*alg_elm:
                        M[i][j] = (M[i][j]+1)%2

    return M


## ----------------- Inputs ----------------- ##

# l = ?
# m = ?
# if BB:
# generators = ['s', 'r']
# relators = [f"s^{l}", f"r^{m}", 's^-1*r*s*r^-1']

generators = ['x', 'y'] # list of group generators (two generators for Symmetric groups).
relators = ['x^3', 'y^2', 'x*y^-1*x*y'] # group relators, must use the same generator names defined in gen.

# Group algebra elements used to make A and B matrices.
a = ['1', 'x', 'x*y']
b = ['1', 'y', 'y*x^2']

## ----------------- Parity Check Matrices ----------------- ##


G, a, b = make_group(generators, relators, a, b)

# A always has action == 'left' and B always has action == right
A = block_matrix(G, a, 'left')
B = block_matrix(G, b, 'right')

H_x = np.hstack((A, B))
H_z = np.hstack((B.T, A.T))

##--------------- Testing ---------------##
rank_H_x = helpers.binary_rank(H_x)
rank_H_z = helpers.binary_rank(H_z)

n : int = len(H_x[0])
k : int = n - rank_H_x - rank_H_z
d : int = bposd.calculate_distance(H_x, H_z)

print(f"[[{n},{k},{d}]]")
# folder_path = 'results_symmetric'
# os.makedirs(folder_path, exist_ok=True)
# file_path = os.path.join(folder_path, f"[{n},{k},{d}].npz")
# with open(file_path, 'wb') as file:
#     np.savez(file, Hx=H_x, Hz=H_z)


