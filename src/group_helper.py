from sage.all import FreeGroup, Integer
import numpy as np
import re

def convert_string_to_expression(exp: list[str], gens):
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


def make_base_group(generators: list[str], rel: list[str]):
    F = FreeGroup(generators)
    F_generators = F._first_ngens(len(generators))

    relators = convert_string_to_expression(rel, F_generators)

    # F_variables = {}
    # F_variables['i'] = F(0)
    # for i, gen in enumerate(generators):
    #     F_variables[gen] = F_generators[i]
    #
    # relators = make_elements_from_expressions(rel, F_variables)

    G = F / relators
    return G


# example expressions = ["s^3", "r", "r^2.s^2.r^-1"]
def make_elements_from_expressions(expressions: list[str], poly_variables):
    elements = []
    for expression in expressions:
        e = poly_variables['i']

        for exp in expression.split('.'):
            # parse expression
            if len(exp) == 1:
                variable, power = exp[0], 1
            else:
                variable, power = exp[0], int(exp[1:])
            e = poly_variables[variable] ** Integer(power)

        elements.append(e)

    return elements


def make_block_matrix(group, algebra, action_is_right: bool):
    elements = group.list()
    m = len(elements)
    Matrix = np.ones(shape=(m, m))

    if action_is_right:
        for algebra_element in algebra:
            for i in range(m):
                for j in range(m):
                    if elements[i] == elements[j] * algebra_element:
                        Matrix[i][j] = (Matrix[i][j] + 1) % 2
    else:
        for algebra_element in algebra:
            for i in range(m):
                for j in range(m):
                    if elements[i] == algebra_element * elements[j]:
                        Matrix[i][j] = (Matrix[i][j] + 1) % 2

    return Matrix

