from __future__ import annotations
import numpy as np
import src.core as core
import random
from copy import deepcopy
import matplotlib.pyplot as plt
import json


class ProposeParameters:
    def __init__(self, l: int = 20, m: int = 20):
        self.l = l
        self.m = m
        self.validate_input()


    def validate_input(self):
        if not 1 <= self.l <= 100:
            raise ValueError("l should be between 1 and 100")
        if not 1 <= self.m <= 100:
            raise ValueError("m should be between 1 and 100")
        pass

    @staticmethod
    def distribute_monomials(all_monomials: list[str], num_A: int | None = None):
        num_monomials = len(all_monomials)
        if num_A is None:
            num_A = num_monomials // 2

        A = all_monomials[:num_A]
        B = all_monomials[num_A:]
        return A, B

    def redraw_l_m_from_normal_distribution(self, threshold: float = 0.01):
        a = np.random.random()
        std_dev_power = 0.5
        if a < threshold:
            new_l = np.random.normal(self.l, self.l ** std_dev_power)
            new_m = np.random.normal(self.m, self.m ** std_dev_power)
            if 1 <= new_l <= 100 and 1 <= new_m <= 100:
                self.l = int(new_l)
                self.m = int(new_m)
        pass

    def draw_random_monomials(self, num_x_monomials: int = 3, num_y_monomials: int = 3):
        x_exponents = np.random.choice(self.l, num_x_monomials, replace=False, p=None)
        y_exponents = np.random.choice(self.m, num_y_monomials, replace=False, p=None)
        monomials = [f"x{i}" for i in x_exponents] + [f"y{i}" for i in y_exponents]
        random.shuffle(monomials)
        return monomials

    def change_one_monomial(self, monomial_expression: list[str], index: int):
        variable, exp = monomial_expression[index][0], int(monomial_expression[index][1:])
        if variable == "x":
            if exp + 1 < self.l:
                monomial_expression[index] = f"x{exp + 1}"
            else:
                monomial_expression[index] = f"x0"
        else:
            if exp + 1 < self.m:
                monomial_expression[index] = f"y{exp + 1}"
            else:
                monomial_expression[index] = f"y0"

        return monomial_expression


    def create_initial_input_parameters(self, num_x_monomials: int = 3, num_y_monomials: int = 3):
        if num_x_monomials > self.l or num_y_monomials > self.m:
            raise ValueError("Number of monomials cannot be greater than l or m")

        all_monomials = self.draw_random_monomials(num_x_monomials, num_y_monomials)
        A, B = self.distribute_monomials(all_monomials)
        return {
            "l" : self.l,
            "m" : self.m,
            "a" : A,
            "b" : B
        }



def search_close_parameters():
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
            code = core.BBCode(inputs["l"], inputs["m"], inputs["a"], inputs["b"], debug=False)
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
        print(f"Best results so far: {max(outputs, key = lambda x: x['score'])}\n\n")

    y = [output["score"] for output in outputs]
    x = [i for i in range(len(y))]
    plt.plot(x, y, 'ro')
    plt.show()

    equivalence_classes = {}
    for item in outputs:
        score = item['score']
        if score not in equivalence_classes:
            equivalence_classes[score] = []
        equivalence_classes[score].append(item)

    #sorting classes by kd2/n value
    # sorted_items = sorted(equivalence_classes.items())
    # equivalence_classes = dict(sorted_items)

    with open("Equivalence_classes.json", 'a') as file:
        json.dump(equivalence_classes, file)

def scaling():
    with open("Equivalence_classes.json", 'r') as file:
        classes = json.load(file)

    param_list=classes[max(classes)]

    for params in param_list:
        y=[params['score']]
        x=[params['n']]
        l=params['l']
        m=params['m']
        for li in range(l+1,max(2*l+1, 2*m+1)):
            code = core.BBCode(li, m, params["a"], params["b"], debug=False)
            n, k, d = code.generate_bb_code(distance_method=3)
            sc=k*(d**2)/n
            y.append(sc)
            x.append(n)
        for mi in range(m,max(2*l+1, 2*m+1)):
            code = core.BBCode(max(2*l+1, 2*m+1), mi, params["a"], params["b"], debug=False)
            n, k, d = code.generate_bb_code(distance_method=3)
            sc = k * (d ** 2) / n
            y.append(sc)
            x.append(n)

        plt.plot(x,y,'o', label=f"A={params['a']}, B={params['b']}")

    plt.xlabel('n')
    plt.ylabel("$kd^2/n$")
    plt.legend()
    plt.show()





if __name__ == "__main__":
    scaling()
