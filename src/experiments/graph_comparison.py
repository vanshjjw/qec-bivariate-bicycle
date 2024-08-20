from src.core import BBCode
from src.helpers.parameters import ProposeParameters
from src.helpers.graphs import Category


def remake_polynomials():
    l = 8
    m = 8
    parameter = ProposeParameters(l, m)
    for i in range(10):
        A, B = parameter.draw_random_monomials(3, 3)
        code = BBCode(l, m, A, B)
        graph1 = code.generate_bb_code()

        a, b = graph1.deconstruct_polynomials("l0")
        print(f"A: {a}, B: {b}")
        a, b = graph1.deconstruct_polynomials("l1")
        print(f"A: {a}, B: {b}")
        a, b = graph1.deconstruct_polynomials("l2")
        print(f"A: {a}, B: {b}")
        a, b = graph1.deconstruct_polynomials("r3")
        print(f"A: {a}, B: {b}")











if __name__ == "__main__":
    remake_polynomials()
