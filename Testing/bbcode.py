import src.core as code
import src.distance_from_gap as dis_gap

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
        "a": ["x0", "x1", "y6"],
        "b": ["y3", "x2", "x3"],
        "answer": [[162, 12, 8]]
    }
    Main["3"] = {
        "l": 9,
        "m": 9,
        "a": ["x0", "y1", "y2"],
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


def run_bbcode_examples():
    Main = {}
    write_raw_data(Main)

    for i in range(len(Main)):
        print(f"Code {i}:")
        print(f"l: {Main[str(i)]['l']}, m: {Main[str(i)]['m']}")
        print(f"A: {Main[str(i)]['a']}")
        print(f"B: {Main[str(i)]['b']}")
        print()

        obj = code.BBCode(Main[str(i)]['l'], Main[str(i)]['m'], Main[str(i)]['a'], Main[str(i)]['b'], debug=False)
        n, k, d = obj.generate_bb_code(distance_method=0)
        H_x, H_z = obj.create_parity_check_matrices()
        d = dis_gap.calculate_distance(H_x, H_z, status_updates=False)

        print(f"Obtained BB code: [{n}, {k}, {d}]")

        if "answer" in Main[str(i)]:
            print(f"Known BB code: {Main[str(i)]['answer']}\n")





if __name__ == "__main__":
    run_bbcode_examples()