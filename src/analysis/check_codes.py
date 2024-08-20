from src.core import BBCode
from src.helpers.polynomials import PolynomialHelper
import numpy as np
import os


def raw_data_more():
    pass


def raw_data_one():
    l = 12
    m = 12
    poly_help = PolynomialHelper(l, m)

    A = ["i", "x", "x2"]
    B = ["i", "y", "y2"]

    A2 = ["i", "x", "y2"]
    B2 = ["i", "y", "x2"]

    codes = {}
    codes["0"] = {
        "l": l,
        "m": m,
        "a": A,
        "b": B
    }
    codes["1"] = {
        "l": l,
        "m": m,
        "a": A2,
        "b": B2,
    }
    codes["3"] = {
        'l': 9,
        'm': 9,
        'a': ['x0', 'x1', 'y1'],
        'b': ['x3', 'y1', 'y2'],
        'answer': [162, 4, 16]
    }
    return codes


def writable_matrix(matrix):
    writable = ""
    for row in matrix:
        writable += "[ " + " ".join(map(str, row)) + " ]" + "\n"
    return writable


def run_and_save_results(save_numpy_matrices = False, display_results = True):
    data = raw_data_one()

    for key in data:
        example = data[key]
        l = example["l"]
        m = example["m"]
        a = example["a"]
        b = example["b"]

        code = BBCode(l, m, a, b, safe_mode=False)
        n, k, d = code.generate_bb_code(distance_method=3)

        if display_results:
            print(f"l: {l}, m: {m}")
            print(f"A: {a}, B: {b}")
            print(f"code: [{n}, {k}, {d}]")
            print("\n\n")

        if save_numpy_matrices:
            folder_path = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(folder_path, 'results_numpy', f"[[{n},{k},{d}]].npz")
            H_x, H_z = code.create_parity_check_matrices()
            with open(file_path, 'wb') as file:
                np.savez(file, Hx=H_x, Hz=H_z)

    print("Completed.")



if __name__ == "__main__":
    run_and_save_results(save_numpy_matrices=False, display_results=True)
    pass