import numpy as np
import src.helpers as helper
import src.core as code
import os

def raw_data(data: dict):
    data["0"] = {
        "l": 6,
        "m": 9,
        "a": ["x0", "y1", "y2"],
        "b": ["y3", "x2", "x4"],
        "answer": [[108, 16, 6]]
    }
    data["1"] = {
        "l": 9,
        "m": 9,
        "a": ["x0", "x1", "y1"],
        "b": ["x3", "y1", "y2"],
        "answer": [[162, 4, 16]]
    }
    data["2"] = {
        "l": 9,
        "m": 9,
        "a": ["x0", "x1", "y6"],
        "b": ["y3", "x2", "x3"],
        "answer": [[162, 12, 8]]
    }
    data["3"] = {
        "l": 9,
        "m": 9,
        "a": ["x0", "y1", "y2"],
        "b": ["y3", "x3", "x6"],
        "answer": [[162, 24, 6]]
    }
    data["4"] = {
        "l": 9,
        "m": 15,
        "a": ["x3", "y1", "y2"],
        "b": ["y3", "x1", "x2"],
        "answer": [[270, 8, 18]]
    }
    data["5"] = {
        "l": 7,
        "m": 7,
        "a": ["x1", "y3", "y4"],
        "b": ["y1", "x3", "x4"],
        "answer": [[98, 6, 12]]
    }
    data["6"] = {
        "l": 9,
        "m": 9,
        "a": ["x3", "y1", "y2"],
        "b": ["y3", "x1", "x2"],
        "answer": [[162, 8, 12]]
    }
    data["7"] = {
        "l": 8,
        "m": 8,
        "a": ["x2", "y1", "y3", "y4"],
        "b": ["y2", "x1", "x2", "x4"],
        "answer": [[128, 14, 12]]
    }


def write_matrix(matrix, file):
    for row in matrix:
        writable = "[ " + " ".join(map(str, row)) + " ]" + "\n"
        file.write(writable)
    file.write("\n\n")




def save_results():
    Main = {}
    raw_data(Main)

    for key in Main:
        example = Main[key]
        l = example["l"]
        m = example["m"]
        a = example["a"]
        b = example["b"]
        c=example["answer"]

        obj = code.BBCode(l, m, a, b, debug=False)
        n, k, d = obj.generate_bb_code(distance_method=3)
        H_x, H_z = obj.create_parity_check_matrices()

        folder = 'Results_npz'
        file_name = f"{c}.npz"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, file_name)

        with open(file_path, 'wb') as file:
            np.savez(file, Hx=H_x, Hz=H_z)

        # with open(f"Results/[[{n}.{k},{d}]].txt", 'wb') as file:
        #     file.write(f"l: {l}\n")
        #     file.write(f"m: {m}\n")
        #     file.write(f"A: {a}\n")
        #     file.write(f"B: {b}\n")
        #
        #     file.write(f"\nBB code: [{n}, {k}, {d}]\n\n")
        #
        #     if "answer" in example:
        #         file.write(f"\nKnown BB code: {example['answer']}\n\n")
        #
        #     file.write("H_x:\n")
        #     write_matrix(H_x, file)
        #     file.write("H_z:\n")
        #     write_matrix(H_z, file)
        #     file.flush()
        #     file.close()




if __name__ == "__main__":
    save_results()
    print("Results saved.")