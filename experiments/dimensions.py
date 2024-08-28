from src.helpers.parameters import ProposeParameters
from src.core_optimised import BBCodeOptimised


def search_dimensions():
    d_lower, d_upper = 3, 20
    num_monomials_min, num_monomials_max = 3, 5
    results = {}

    print("Begin.\n\n")
    for j in range(num_monomials_min, num_monomials_max + 1):
        num_x_monomials = j
        num_y_monomials = j

        for i in range(d_lower, d_upper + 1):
            if j > i:
                break

            l = i
            m = i
            propose = ProposeParameters(l, m)
            code_cached = BBCodeOptimised(l, m)

            average_k = 0
            average_d = 0
            num_non_zero_k = 0
            num_shots = 50

            for _ in range(num_shots):
                A, B = propose.distribute_monomials(propose.draw_random_monomials(j, j))
                # A and B both have j-terms each, a mix of monomials of the form x^a, y^b
                # They do not have any combined terms of the form  x^a.y^b

                n, k, d = code_cached.set_expressions(A, B).generate_bb_code(distance_method=4)
                # code cached stores all variables of the form x^a, y^b, so just set your polynomial expressions
                # and generate the code
                # distance method 4 is bposd. method 3 requires GAP, methods 2 ad 1 are incomplete, and 0 will skip
                # the distance calculation

                if k != 0:
                    num_non_zero_k += 1
                    average_k += k
                    average_d += d

            print(f"dimension = {m}, num_x_monomials = {j}   (n = {2 * l * m})")
            if num_non_zero_k > 0:
                results[(i, j)] = {
                    "non-zero codes": f'{num_non_zero_k}/{num_shots}',
                    "average_k": round(average_k / num_non_zero_k, 2),
                    "average_d": round(average_d / num_non_zero_k, 2)
                }
                print(results[(i, j)])
            print("\n\n")

    print("Results:")
    print(results)





if __name__ == "__main__":
    search_dimensions()
    pass





