import numpy as np
import src.core as core


class Proposal:
    def __init__(self, l: int, m: int):
        self.l = l
        self.m = m
        self.validate_input()


    def validate_input(self):
        if not 1 <= self.l <= 100:
            raise ValueError("l should be between 1 and 100")
        if not 1 <= self.m <= 100:
            raise ValueError("m should be between 1 and 100")


    def draw_l_m_from_normal_distribution(self):
        pass


    def draw_monomials(self, num_x_monomials: int = 3, num_y_monomials: int = 3):
        x_exponents = np.random.choice(self.l, num_x_monomials, replace=False, p=None)
        y_exponents = np.random.choice(self.m, num_y_monomials, replace=False, p=None)

        return [f"x{i}" for i in x_exponents] + [f"y{i}" for i in y_exponents]


    def create_input_parameters(self, num_x_monomials: int = 3, num_y_monomials: int = 3):
        all_monomials = self.draw_monomials(num_x_monomials, num_y_monomials)
        num_monomials = len(all_monomials)

        place_in_A = np.random.choice(num_monomials, num_monomials // 2, replace=False, p=None)

        A = [all_monomials[i] for i in place_in_A]
        B = [all_monomials[i] for i in range(num_monomials) if i not in place_in_A]

        return {
            "l" : self.l,
            "m" : self.m,
            "a" : A,
            "b" : B
        }



def random_search():
    l = 9
    m = 9
    num_Trials = 1000
    p = Proposal(l, m)

    for i in range(num_Trials):
        inputs = p.create_input_parameters()
        print(inputs)
        code = core.BBCode(inputs["l"], inputs["m"], inputs["a"], inputs["b"], debug=False)
        n, k, d = code.generate_bb_code(distance_method=0)
        if k != 0:
            print("inputs: ", inputs)
            print(f"n: {n}, k: {k}, d: {d} \n")



if __name__ == "__main__":
    random_search()
