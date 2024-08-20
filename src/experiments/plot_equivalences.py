import numpy as np
import src.core as core
from src.helpers.parameters import ProposeParameters
from copy import deepcopy
import matplotlib.pyplot as plt
import json


def plot_equivalence_classes_scaling():
    with open("Equivalence_classes.json", 'r') as file:
        classes = json.load(file)

    param_list = classes[max(classes)]

    for params in param_list:
        y = [params['score']]
        x = [params['n']]
        l = params['l']
        m = params['m']

        for li in range(l + 1, max(2 * l + 1, 2 * m + 1)):
            code = core.BBCode(li, m, params["a"], params["b"], safe_mode=False)
            n, k, d = code.generate_bb_code(distance_method=3)
            sc = k * (d ** 2) / n
            y.append(sc)
            x.append(n)

        for mi in range(m, max(2 * l + 1, 2 * m + 1)):
            code = core.BBCode(max(2 * l + 1, 2 * m + 1), mi, params["a"], params["b"], safe_mode=False)
            n, k, d = code.generate_bb_code(distance_method=3)
            sc = k * (d ** 2) / n
            y.append(sc)
            x.append(n)

        plt.plot(x, y, 'o', label=f"A={params['a']}, B={params['b']}")

    plt.xlabel('n')
    plt.ylabel("$kd^2/n$")
    plt.legend()
    plt.show()


def create_equivalence_classes(outputs):
    equivalence_classes = {}
    for item in outputs:
        score = item['score']
        if score not in equivalence_classes:
            equivalence_classes[score] = []
        equivalence_classes[score].append(item)

    # sorting classes by kd2/n value
    # sorted_items = sorted(equivalence_classes.items())
    # equivalence_classes = dict(sorted_items)

    with open("Equivalence_classes.json", 'a') as file:
        json.dump(equivalence_classes, file)


def search_close_parameters(create_equivalence = False):
    l = 8
    m = 8
    num_x_monomials = 4
    num_y_monomials = 4
    num_inputs = 2
    num_shots = num_x_monomials * l + num_y_monomials * m

    proposal = ProposeParameters(l, m)
    outputs = []

    for i in range(num_inputs):
        inputs = proposal.create_initial_input_parameters(num_x_monomials, num_y_monomials)
        print(f"Initial inputs: {inputs} for {num_shots} runs\n\n")

        for j in range(num_shots):
            code = core.BBCode(inputs["l"], inputs["m"], inputs["a"], inputs["b"], safe_mode=False)
            n, k, d = code.generate_bb_code(distance_method=3)

            if k != 0:
                results = deepcopy(inputs)
                results["n"] = n
                results["k"] = k
                results["d"] = d
                results["score"] = np.round(k * d * d / n, 3)
                outputs.append(results)
                print(f"Trial {j}: Results: {results}")

            # change inputs
            if j < num_x_monomials * l:
                inputs["a"] = proposal.change_one_monomial(inputs["a"], j // l)
            else:
                inputs["b"] = proposal.change_one_monomial(inputs["b"], (j - num_x_monomials * l) // m)

        print("\n\nCurrent input complete\n\n")
        print(f"Best results so far: {max(outputs, key = lambda key: key['score'])}\n\n")

    y = [output["score"] for output in outputs]
    x = [i for i in range(len(y))]
    plt.plot(x, y, 'ro')
    plt.show()

    if create_equivalence:
        create_equivalence_classes(outputs)

    pass


if __name__ == "__main__":
    search_close_parameters(create_equivalence = False)




