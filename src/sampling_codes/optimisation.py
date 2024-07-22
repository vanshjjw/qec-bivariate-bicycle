import numpy as np
from numpy import random
from proposal import Proposal
from typing import Callable
import src.core as core

# def step(x, s):
#     """
#     Gaussian proposal function for simulated annealing algorithm.
#     """
#     d = 7*(2*random.random(2)-1)
#     a = random.random()
#     # gaussian with mean 0 and standard deviation s
#     p = (1/(s*np.sqrt(2*np.pi)))*np.exp(-(d**2)/(2*(s**2)))
#     while p[0] < a and p[1] < a:
#         d = 7*(2*random.random(2)-1)
#         a = random.random()
#         p = (1/(s*np.sqrt(2*np.pi)))*np.exp(-(d**2)/(2*(s**2)))
#     return np.array(x)+d

def func(inputs):
    code = core.BBCode(inputs["l"], inputs["m"], inputs["a"], inputs["b"], debug=False)
    n, k, d = code.generate_bb_code(distance_method=3)
    rate = k / (2 * n)
    return 10 * rate + d


def bbcode_optimisation__function(p : Proposal):
    input_parameters = p.create_input_parameters()
    return input_parameters, func(input_parameters)


def simulated_annealing(f : Callable, T0 : float, n : int):
    """
    Simulated annealing algorithm with initial temperature T0,
    starting point x0, n iterations and gaussian proposal with
    standard deviation s.
    """
    p = Proposal
    Initial_Value = f(p)
    T = T0
    best_input, best_output = x0, Initial_Value
    all_outputs = []

    for i in range(n):
        T /= 2

        new_input, new_output = f(p)

        if new_output > best_output:
            best_input, best_output = new_input, new_output
        else:
            diff = best_output - new_output
            # random number between 0 and 1
            a = random.random()
            if a < np.exp(diff/T):
                best_input, best_output = new_input, new_output

        all_outputs.append(Initial_Value)

    return best_input, best_output, all_outputs



if __name__ == "__main__":
    T0 = 1000
    n = 1000

    i, o, all = simulated_annealing(bbcode_optimisation__function, T0, n)

    print(f"")