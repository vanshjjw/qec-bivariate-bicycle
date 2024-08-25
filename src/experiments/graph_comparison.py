from src.core import BBCode
from src.helpers.polynomials import PolynomialHelper


def remake_polynomials():
    l = 16
    m = 16
    A = ['i', f'x']
    B = ['i', f'y']
    poly_help = PolynomialHelper(l, m)
    for i in range(1, 5):
        code = BBCode(l, m, A, B)
        n, k, d = code.generate_bb_code(distance_method=3)

        print(f"A : {A}: \nB: {B} \n")
        print(f"code: [{n}, {k}, {d}]")
        print("\n\n")

        A = poly_help.multiply_polynomials(A, A)
        B = poly_help.multiply_polynomials(B, B)















if __name__ == "__main__":
    remake_polynomials()
