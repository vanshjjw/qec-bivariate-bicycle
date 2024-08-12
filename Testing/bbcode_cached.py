from src.core_cached import BBCodeCached
from src.core import BBCode
import src.helpers as helper
import numpy as np

def write_raw_data(Main: dict):
    Main["0"] = {
        "l": 6,
        "m": 9,
        "a": ["x0", "y1", "y2"],
        "b": ["y3", "x2", "x4"],
        "answer": [[108, 16, 6]]
    }
    Main["1"] = {
        "l": 9,
        "m": 9,
        "a": ["x0", "x1", "y1"],
        "b": ["x3", "y1", "y2"],
        "answer": [[162, 4, 16]]
    }
    Main["2"] = {
        "l": 9,
        "m": 9,
        "a": ["i", "x1", "y6"],
        "b": ["y3", "x2", "x3"],
        "answer": [[162, 12, 8]]
    }
    Main["3"] = {
        "l": 9,
        "m": 9,
        "a": ["i", "y1", "y2"],
        "b": ["y3", "x3", "x6"],
        "answer": [[162, 24, 6]]
    }
    Main["4"] = {
        "l": 9,
        "m": 15,
        "a": ["x3", "y1", "y2"],
        "b": ["y3", "x1", "x2"],
        "answer": [[270, 8, 18]]
    }
    Main["5"] = {
        "l": 7,
        "m": 7,
        "a": ["x1", "y3", "y4"],
        "b": ["y1", "x3", "x4"],
        "answer": [[98, 6, 12]]
    }
    Main["6"] = {
        "l": 9,
        "m": 9,
        "a": ["x3", "y1", "y2"],
        "b": ["y3", "x1", "x2"],
        "answer": [[162, 8, 12]]
    }
    Main["7"] = {
        "l": 8,
        "m": 8,
        "a": ["x2", "y1", "y3", "y4"],
        "b": ["y2", "x1", "x3", "x4"],
        "answer": [[128, 14, 12]]
    }
    Main["8"] = {
        "l": 12,
        "m": 12,
        "a": ["x3", "y2", "y7"],
        "b": ["y3", "x1", "x2"],
        "answer": [[288, 12, 18]]
    }



def run_bbcode_cached_examples():
    Main = {}
    write_raw_data(Main)

    for i in range(len(Main)):
        print(f"Code {i}:")
        print(f"l: {Main[str(i)]['l']}, m: {Main[str(i)]['m']}")
        print(f"A: {Main[str(i)]['a']}")
        print(f"B: {Main[str(i)]['b']}")
        print()

        code = BBCodeCached(Main[str(i)]['l'], Main[str(i)]['m'], safe_mode=True)
        code.set_expressions(Main[str(i)]['a'], Main[str(i)]['b'])
        n, k, d = code.generate_bb_code(distance_method=4)

        print(f"Obtained BB code: [{n}, {k}, {d}]")

        if "answer" in Main[str(i)]:
            print(f"Known BB code: {Main[str(i)]['answer']}")
            n_answer, k_answer, d_answer = Main[str(i)]['answer'][0]
            print("right answer? ", (n == n_answer) and (k == k_answer) and (d_answer < d * 1.20))
            print("\n\n")



if __name__ == "__main__":
    run_bbcode_cached_examples()