import numpy as np
from numpy import random

def step(x, s):
    """
    Gaussian proposal function for simulated annealing algorithm.
    """
    d = 7*(2*random.random(2)-1)
    a = random.random()
    # gaussian with mean 0 and standard deviation s
    p = (1/(s*np.sqrt(2*np.pi)))*np.exp(-(d**2)/(2*(s**2)))
    while p[0] < a and p[1] < a:
        d = 7*(2*random.random(2)-1)
        a = random.random()
        p = (1/(s*np.sqrt(2*np.pi)))*np.exp(-(d**2)/(2*(s**2)))
    return np.array(x)+d


def simulated_annealing(f,T0, x0, n, s):
    """
    Simulated annealing algorithm with initial temperature T0,
    starting point x0, n iterations and gaussian proposal with
    standard deviation s.
    """
    x0 = np.array(x0)
    E0 = f(x0)
    T = T0
    bestx, bestE = x0, E0
    E = []
    I = []
    for i in range(n):
        I.append(i)
        T /= 2
        xi = step(x0, s)
        Ei = f(xi)
        if Ei > bestE:
            bestx, bestE = xi, Ei
        diff = Ei-E0
        a = random.random()
        if (diff > 0) or (a < np.exp(diff/T)):
            x0, E0 = xi, Ei
        E.append(E0)
    return bestx, I, E

