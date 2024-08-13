from sage.all import PolynomialRing, GF


def factorise(polynomial_powers: list[(int, int)]) -> (list[str], list[int]):
    ring = PolynomialRing(GF(2), ['x', 'y'])
    x, y = ring.gens()

    p = 0
    for power in polynomial_powers:
        p += (x ** power[0]) * (y ** power[1])
    factors = p.factor()

    answer: list[str] = []
    answer_exp: list[int] = []

    for factor, multiplicity in factors:
        answer.append(str(factor))
        answer_exp.append(int(multiplicity))

    return answer, answer_exp

