from src.core_generalised import GeneralGroupAlgebraCodes

def codes(codes: dict):
    codes["0"] = {
        "a": ['x3', 'y2','y7'],
        "b": ['y3','x', 'x2'],
        "order": 5
    }
    codes["1"] = {
        "a": ['i', 'y', 'x.y7'],
        "b": ['i', 'x', 'x10.y4']
    }
    return codes



def compare_groups():
    Main = {}
    distance_method = 3
    Main = codes(Main)

    for i in range(len(Main)):
        example = Main[str(i)]
        code = GeneralGroupAlgebraCodes().set_expression(example["a"], example["b"]).set_symmetric_base_group(example["order"])

        n, k, d = code.generate_bb_code(distance_method=distance_method)

        print(f"order: {example['order']}")
        print(f"A: {example['a']}")
        print(f"B: {example['b']}")
        print(f"\nRequired BB code: [{n}, {k}, {d}]")



if __name__ == "__main__":
    compare_groups()
    pass