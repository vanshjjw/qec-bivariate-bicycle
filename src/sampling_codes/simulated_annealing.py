import numpy as np
from numpy import random
from proposal import Proposal
from typing import Callable
import src.core as core


def bbcode_optimisation__function(p : Proposal):
    inputs = p.create_input_parameters()
    code = core.BBCode(inputs["l"], inputs["m"], inputs["a"], inputs["b"], debug=False)
    n, k, d = code.generate_bb_code(distance_method=3)

    inputs["n"] = n
    inputs["k"] = k
    inputs["d"] = d
    value = - k / n

    return inputs, value


# func accepts a Proposal object (fixed l and m for now), guesses input parameters randomly, and returns the parameters
# with the (negative) encoding rate as the value to be minimised

def simulated_annealing(func : Callable, Temperature : float, num_iterations : int, l : int = 9, m : int = 9,
                        T_reduce_factor : int = 5):

    p = Proposal(l = l, m = m)

    min_input, min_output = func(p)
    abs_best_input, abs_best_output = min_input, min_output

    all_outputs = [min_output]
    all_inputs = [min_input]

    iteration = 1
    while len(all_outputs) < num_iterations:

        current_input, current_output = func(p)
        if current_input["d"] >= current_input["n"]:
            # unphysical code
            continue
        else:
            print(f"iteration {iteration} of {num_iterations}")
            iteration += 1

        Temperature = Temperature / T_reduce_factor

        if current_output <= min_output:
            min_input, min_output = current_input, current_output
            if current_output < abs_best_output:
                abs_best_input, abs_best_output = current_input, current_output
        else:
            diff = current_output - min_output
            # random number between 0 and 1
            a = random.random()
            if a < np.exp(- diff / Temperature):
                print(f"accepting worse solution at T = {Temperature}, diff {diff}, iteration {iteration} "
                      f"with probability {np.exp(- diff / Temperature)}")
                min_input, min_output = current_input, current_output

        all_outputs.append(current_output)
        all_inputs.append(current_input)

    return abs_best_input, abs_best_output, all_inputs, all_outputs



def run_search():
    T = 100
    T_reduce = 5
    num_iter = 5
    l = 9
    m = 9
    write_results = True
    optimise = "encoding rate"

    print(
        f"Running simulated annealing to optimise {optimise} with parameters: Temperature: {T}, "
        f"T_reduce_factor: {T_reduce}, "
        f"num_iterations: {num_iter}, \nfor codes with l: {l}, m: {m} \n\n"
    )

    best_input, best_output, all_ins, all_outs = simulated_annealing(
        bbcode_optimisation__function,
        Temperature = T,
        num_iterations = num_iter,
        l = l,
        m = m,
        T_reduce_factor = T_reduce

    )

    print("\n\n")
    print(f"best input found {best_input}")
    print(f"best optimised value {best_output}")

    if write_results:
        with open("codes", "a") as f:
            f.write(f"\n\nl = {l}, m = {m} simulated annealing with {optimise} optimised: \n")
            for i in all_ins:
                f.write(str(i) + "\n")
            f.flush()
            f.close()

        print("Results saved.")





if __name__ == "__main__":
    run_search()
