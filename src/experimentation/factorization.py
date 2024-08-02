from src.experimentation.propose_parameters import ProposeParameters
import numpy as np
import src.helpers as helper
import src.core as core


def find_generators_for_graph(A: list[str], B: list[str], l: int, m: int) -> np.ndarray:
    generators : list[str] = []
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            generators.append(f"x{i}y{j}")






def factorizable():
    p = ProposeParameters(l = 16, m = 16)
    num_shots = 10000


    pass