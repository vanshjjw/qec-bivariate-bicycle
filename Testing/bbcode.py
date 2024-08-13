from src.core import BBCode
import json

def check_custom_codes(codes: dict):
    codes["0"] = {
        "l": 6,
        "m": 9,
        "a": ["x0", "y1", "y2"],
        "b": ["y3", "x2", "x4"],
        "answer": [108, 16, 6]
    }
    codes["1"] = {
        "l": 9,
        "m": 9,
        "a": ["x0", "x1", "y1"],
        "b": ["x3", "y1", "y2"],
        "answer": [162, 4, 16]
    }


def run_bbcode_examples(custom_codes = False):
    Main = {}

    if custom_codes:
        check_custom_codes(Main)
    else:
        with open("known_codes", "r") as file:
            json_readable = file.read().replace("\'", "\"")
            Main = json.loads(json_readable)

    for i in range(len(Main)):
        print(f"Code {i}:")
        print(f"l: {Main[str(i)]['l']}, m: {Main[str(i)]['m']}")
        print(f"A: {Main[str(i)]['a']}")
        print(f"B: {Main[str(i)]['b']}")
        print()

        code = BBCode(Main[str(i)]['l'], Main[str(i)]['m'], Main[str(i)]['a'], Main[str(i)]['b'], safe_mode=False)
        n, k, d = code.generate_bb_code(distance_method=4)

        print(f"Obtained BB code: [{n}, {k}, {d}]")

        if 'answer' in Main[str(i)]:
            print(f"Known BB code: {Main[str(i)]['answer']}")
            n_answer, k_answer, d_answer = Main[str(i)]['answer']
            print("right answer? ", (n == n_answer) and (k == k_answer) and (d_answer < d * 1.20))
            print("\n\n")



if __name__ == "__main__":
    run_bbcode_examples(False)