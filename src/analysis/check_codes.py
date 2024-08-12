import json
import numpy as np
import src.core as core
import os


def raw_data():
    # add data to this dictionary in the format of the examples below
    # run add_data_to_json() to save data to the known codes file
    new_codes = {}
    new_codes["0"] = {
        "l": 6,
        "m": 9,
        "a": ["x0", "y1", "y2"],
        "b": ["y3", "x2", "x4"],
        "answer": [108, 16, 6]
    }
    new_codes["1"] = {
        "l": 9,
        "m": 9,
        "a": ["x0", "x1", "y1"],
        "b": ["x3", "y1", "y2"],
        "answer": [162, 4, 16]
    }
    return new_codes


def save_raw_data_file(data):
    with open("known_codes", "w") as file:
        file.write("{\n")
        for i, key in enumerate(data):
            file.write(f"\"{key}\": {str(data[key])}")
            if i < len(data) - 1:
                file.write(",")
            file.write("\n")
        file.write("}")
        file.flush()
        file.close()


def add_raw_data_to_json():
    with open("known_codes", "r") as file:
        old_codes = json.loads(file.read().replace("\'", "\""))
        new_codes = raw_data()

        num_codes = len(old_codes)
        num_codes_to_add = len(new_codes)

        for i in range(num_codes, num_codes + num_codes_to_add):
            if str(i) in old_codes:
                raise ValueError(f"code numbered {i} already exists")
            old_codes[str(i)] = new_codes[str(i - num_codes)]

    save_raw_data_file(old_codes)


def write_matrix(matrix, file):
    for row in matrix:
        writable = "[ " + " ".join(map(str, row)) + " ]" + "\n"
        file.write(writable)
    file.write("\n\n")



# TODO - wsl does not naturally have the path to results directory saved. Need to give it the relative path from root
def run_and_save_results(save_as_numpy = False):
    with open("known_codes", "r") as file:
        data = json.loads(file.read().replace("\'", "\""))

    for key in data:
        example = data[key]
        l = example["l"]
        m = example["m"]
        a = example["a"]
        b = example["b"]
        c = example["answer"]

        obj = core.BBCode(l, m, a, b, safe_mode=False)
        n, k, d = obj.generate_bb_code(distance_method=3)
        H_x, H_z = obj.create_parity_check_matrices()


        if save_as_numpy:
            file_path = os.path.join('results_numpy', f"[[{n}.{k},{d}]].npz")
            with open(file_path, 'wb') as file:
                np.savez(file, Hx = H_x, Hz = H_z)
            return

        with open(f"results/[[{n}.{k},{d}]].txt", 'wb') as file:
            file.write(f"l: {l}\n")
            file.write(f"m: {m}\n")
            file.write(f"A: {a}\n")
            file.write(f"B: {b}\n")

            file.write(f"\nBB code: [{n}, {k}, {d}]\n\n")

            if "answer" in example:
                file.write(f"\nKnown BB code: {example['answer']}\n\n")

            file.write("H_x:\n")
            write_matrix(H_x, file)
            file.write("H_z:\n")
            write_matrix(H_z, file)
            file.flush()
            file.close()




if __name__ == "__main__":
    pass