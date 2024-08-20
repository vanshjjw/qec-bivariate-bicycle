from src.polynomial_helper import PolynomialHelper
from src.propose_parameters import ProposeParameters
from src.core import BBCode

def raw_data():
    l = 12
    m = 12
    A1 = ["i", "x", "x2"]
    B1 = ["i", "y", "y2"]

    A2 = ["i", "x", "y2"]
    B2 = ["i", "y", "x2"]

    a = {
        "l": l,
        "m": m,
        "a": A1,
        "b": B1
    }
    b = {
        "l": l,
        "m": m,
        "a": A2,
        "b": B2
    }
    return a, b



def compare_graphs():
    d1, d2 = raw_data()

    code1 = BBCode(d1["l"], d1["m"], d1["a"], d1["b"], safe_mode=False)
    code2 = BBCode(d2["l"], d2["m"], d2["a"], d2["b"], safe_mode=False)

    graph1 = code1.make_graph()
    graph2 = code2.make_graph()
    pass




if __name__ == "__main__":
    compare_graphs()
