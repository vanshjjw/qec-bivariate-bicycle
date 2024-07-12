# Ideally want to create a file that contains the known codes
# and read it as a json file. But currently having trouble with
# the format of the data I have used


if __name__ == "__main__":
    with open("known_codes.txt", "w") as file:
        Main = {}
        A = {
            "l":6,
            "m":6,
            "a":["x3", "y1", "y2"],
            "b":["y3", "x1", "x2"],
            "answer":[72, 12, 6]
        }
        Main["1"] = A

        A = {
            "l": 15,
            "m": 3,
            "a": ["x9", "y1", "y2"],
            "b": ["y0", "x2", "x7"],
            "answer": [90, 8, 10]
        }
        Main["2"] = A

        A = {
            "l": 9,
            "m": 6,
            "a": ["x3", "y1", "y2"],
            "b": ["y3", "x1", "x2"],
            "answer": [108, 8, 10]
        }
        Main["3"] = A

        A = {
            "l": 12,
            "m": 6,
            "a": ["x3", "y1", "y2"],
            "b": ["y3", "x1", "x2"],
            "answer": [144, 12, 12]
        }
        Main["4"] = A

        A = {
            "l": 12,
            "m": 12,
            "a": ["x3", "y1", "y2"],
            "b": ["y3", "x1", "x2"],
            "answer": [288, 12, 18]
        }
        Main["5"] = A

        A = {
            "l": 30,
            "m": 6,
            "a": ["x9", "y1", "y2"],
            "b": ["y3", "x25", "x26"],
            "answer": [360, 12, 24]
        }
        Main["6"] = A

        A = {
            "l": 21,
            "m": 18,
            "a": ["x3", "y10", "y17"],
            "b": ["y5", "x3", "x19"],
            "answer": [756, 16, 34]
        }
        Main["7"] = A

        file.write(str(Main))
        file.flush()
        file.close()

    print("File created successfully")
    pass

