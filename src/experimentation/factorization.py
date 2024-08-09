from src.polynomials import PolynomialHelper, PolynomialToGraphs
from src.experimentation.propose_parameters import ProposeParameters
from src.core import BBCode
import src.helpers as helper


def factorize():
    l = 12
    m = 12
    parameters = ProposeParameters(l, m)
    poly_help = PolynomialHelper(l, m)

    num_shots = 8000
    counter = 0

    for i in range(1, num_shots):
        if i % 200 == 0:
            print(f"Trial {i} completed.")

        A = parameters.draw_disconnected_monomials(3, 0)
        B = parameters.draw_disconnected_monomials(0, 3)

        code = BBCode(l, m, A, B)
        n, k, d = code.generate_bb_code(distance_method=0)

        if k != 0:
            counter += 1

    print(f"rate of univariate polynomial: {counter / num_shots}")

    counter = 0

    for i in range(1, num_shots):
        if i % 200 == 0:
            print(f"Trial {i} completed.")

        A, B = parameters.distribute_monomials(parameters.draw_random_monomials(3, 3))

        code = BBCode(l, m, A, B)
        n, k, d = code.generate_bb_code(distance_method=0)

        if k != 0:
            counter += 1

    print(f"rate of random polynomial: {counter / num_shots}")











if __name__ == "__main__":
    factorize()
    pass