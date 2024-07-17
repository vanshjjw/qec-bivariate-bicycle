import src.core as code
def write_raw_data(Main: dict):
    Main["0"] = {
        "l": 6,
        "m": 6,
        "a": ["x3", "y1", "y2"],
        "b": ["y3", "x1", "x2"],
        "answer": [72, 12, 6]
    }
    Main["1"] = {
        "l": 15,
        "m": 3,
        "a": ["x9", "y1", "y2"],
        "b": ["y0", "x2", "x7"],
        "answer": [90, 8, 10]
    }
    Main["2"] = {
        "l": 9,
        "m": 6,
        "a": ["x3", "y1", "y2"],
        "b": ["y3", "x1", "x2"],
        "answer": [108, 8, 10]
    }
    Main["3"] = {
        "l": 12,
        "m": 6,
        "a": ["x3", "y1", "y2"],
        "b": ["y3", "x1", "x2"],
        "answer": [144, 12, 12]
    }
    Main["4"] = {
        "l": 12,
        "m": 12,
        "a": ["x3", "y1", "y2"],
        "b": ["y3", "x1", "x2"],
        "answer": [288, 12, 18]
    }
    Main["5"] = {
        "l": 30,
        "m": 6,
        "a": ["x9", "y1", "y2"],
        "b": ["y3", "x25", "x26"],
        "answer": [360, 12, 24]
    }
    Main["6"] = {
        "l": 21,
        "m": 18,
        "a": ["x3", "y10", "y17"],
        "b": ["y5", "x3", "x19"],
        "answer": [756, 16, 34]
    }


def run_bbcode_examples():
    Main = {}
    write_raw_data(Main)

    for i in range(len(Main)):
        print(f"Code {i}:")
        print(f"l: {Main[str(i)]['l']}, m: {Main[str(i)]['m']}")
        print(f"A: {Main[str(i)]['a']}")
        print(f"B: {Main[str(i)]['b']}")
        print(f"Answer: {Main[str(i)]['answer']}")
        print()

        obj = code.BBCode(Main[str(i)]['l'], Main[str(i)]['m'], Main[str(i)]['a'], Main[str(i)]['b'], debug=False)
        n, k, d = obj.generate_bb_code()
        print(f"Required BB code: [{n}, {k}, {d}]")

        if "answer" in Main[str(i)]:
            print(f"answer: {Main[str(i)]['answer']}")





if __name__ == "__main__":
    run_bbcode_examples()