from sage.all import FreeGroup, Integer
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


def make_group(generators: list[str], rel: list[str], a: list[str], b: list[str]):
    F = FreeGroup(generators)
    F_generators = F._first_ngens(len(generators))
    relators = convert_string_to_expression(rel, F_generators)

    G = F / relators
    G_generators = G.gens()

    a = convert_string_to_expression(a, G_generators)
    b = convert_string_to_expression(b, G_generators)

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

generators = ['x', 'y'] #list of group generators (two generators for Symmetric groups).
relators = ['x^3', 'y^2', 'x*y^-1*x*y'] # group relators, must use the same generator names defined in gen.

# Group algebra elements used to make A and B matrices.
a = ['1','x','x*y']
b = ['1','y','y*x^2']

## ----------------- Parity Check Matrices ----------------- ##


G, a, b = make_group(generators, relators, a, b)

print(G)

# A always has action == 'left' and B always has action == right
A = block_matrix(G, a, 'left')
B = block_matrix(G, b, 'right')

H_x = np.hstack((A, B))
H_z = np.hstack((B.T, A.T))
print(H_x@H_z.T %2)




