from src.core import BBCode
from src.core_cached import BBCodeCached
from src.propose_parameters import ProposeParameters
import numpy as np
import random
import time


def benchmark_cache():
    num_outer_shots = 5
    num_inner_shots = 100
    distance_method = 3

    code_performance = []
    code_cached_performance = []

    for i in range(num_outer_shots):
        l, m = random.randint(9, 22), random.randint(9, 22)
        parameters = ProposeParameters(l, m)
        print(f"l = {l}, m = {m}")

        A_exps = []
        B_exps = []

        for j in range(num_inner_shots):
            A, B = parameters.distribute_monomials(parameters.draw_random_monomials(3, 3))
            A_exps.append(A)
            B_exps.append(B)


        print(f"Benchmarking code cache for l = {l}, m = {m}")
        # benchmark cached_code
        T1 = time.time()

        code_cached = BBCodeCached(l, m)
        for j in range(num_inner_shots):
            A = A_exps[j]
            B = B_exps[j]
            n, k, d = code_cached.set_expressions(A, B).generate_bb_code(distance_method=distance_method)

        T2 = time.time()
        code_cached_performance.append(T2 - T1)

        print(f"Benchmarking code for l = {l}, m = {m}")
        # benchmark code
        T1 = time.time()

        for j in range(num_inner_shots):
            A = A_exps[j]
            B = B_exps[j]
            code = BBCode(l, m, A, B)
            n, k, d = code.generate_bb_code(distance_method=distance_method)

        T2 = time.time()
        code_performance.append(T2 - T1)


    print("\n\n")
    print(f"caching performance: {code_cached_performance}")
    print(f"code performance: {code_performance}")

    print(f"Total caching performance: {sum(code_cached_performance)}")
    print(f"Total code performance: {sum(code_performance)}")




def benchmark_matrix_construction_from_expression():
    num_shots = 5000
    l = 12
    m = 12

    #
    parameters = ProposeParameters(l, m)
    polynomials = [parameters.draw_bivariate_monomials(3) for _ in range(num_shots)]


    code_cached = BBCodeCached(l, m)
    method_1_verifications = {}
    method_2_verifications = {}

    # method 1

    T1 = time.time()

    for i in range(num_shots):
        m = code_cached.construct_matrix_from_expression(polynomials[i])
        if i % 100 == 0:
            print(f"Method 1: {i} completed.")
            method_1_verifications[i] = m

    T2 = time.time()
    print(f"Method 1: {T2 - T1}")


    # method 2
    T1 = time.time()

    for i in range(num_shots):
        m = code_cached.construct_matrix_from_expression_2(polynomials[i])
        if i % 100 == 0:
            print(f"Method 2: {i} completed.")
            method_2_verifications[i] = m

    T2 = time.time()
    print(f"Method 2: {T2 - T1}")

    for i in range(0, num_shots, 100):
        m1 = method_1_verifications[i]
        m2 = method_2_verifications[i]
        print(f"equal: {np.array_equal(m1, m2)}")

    pass



if __name__ == "__main__":
    benchmark_matrix_construction_from_expression()
    pass