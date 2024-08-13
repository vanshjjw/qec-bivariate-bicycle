import galois
import subprocess
import json
import ast

class PolynomialHelper:
    def __init__(self, l, m):
        self.l = l
        self.m = m
    
    def __construct_expression(self, x_power: int, y_power: int):
        x_power = x_power % self.l
        y_power = y_power % self.m
        
        if x_power == 0 and y_power == 0:
            return "i"
        if x_power == 0:
            return f"y{y_power}"
        if y_power == 0:
            return f"x{x_power}"
        return f"x{x_power}.y{y_power}"


    def __construct_powers(self, monomial: str):
        x_power = 0
        y_power = 0
        for mu in monomial.split("."):
            if mu[0] == "x":
                x_power += int(mu[1:])
            if mu[0] == "y":
                y_power += int(mu[1:])
        return x_power % self.l, y_power % self.m


    def construct_expression_from_powers(self, polynomial_powers: list[(int, int)]):
        return [self.__construct_expression(x_power, y_power) for x_power, y_power in polynomial_powers]


    def construct_powers_from_expression(self, polynomial_expression: list[str]):
        return [self.__construct_powers(monomial) for monomial in polynomial_expression]


    def multiply_m1_and_m2_inverse(self, m1: str, m2: str):
        x_power, y_power = 0, 0
        
        for mu in m1.split("."):
            if mu[0] == "x":
                x_power += int(mu[1:])
            if mu[0] == "y":
                y_power += int(mu[1:])

        for mu in m2.split("."):
            if mu[0] == "x":
                x_power -= int(mu[1:])
            if mu[0] == "y":
                y_power -= int(mu[1:])

        return x_power % self.l, y_power % self.m


    def multiply_polynomials(self, poly1: list[str], poly2: list[str]):
        result = []
        for value1 in poly1:
            for value2 in poly2:
                multiplicands = value1.split(".") + value2.split(".")
                x_power = 0
                y_power = 0

                for mu in multiplicands:
                    if mu[0] == "x":
                        x_power += int(mu[1:])
                    if mu[0] == "y":
                        y_power += int(mu[1:])

                answer = self.__construct_expression(x_power, y_power)
                if answer in result:
                    result.remove(answer)
                else:
                    result.append(answer)

        return result


    def galois_factors_to_expression(self, factors: list[galois.Poly], exponents: list[int], is_x : bool):
        answer = []
        answer_exp = []
        for f, exp in zip(factors, exponents):
            non_zero_degrees = f.nonzero_degrees
            if len(non_zero_degrees) == 1:
                continue

            powers = [(d, 0) if is_x else (0, d) for d in non_zero_degrees]
            polynomial = self.construct_expression_from_powers(powers)

            answer.append(polynomial)
            answer_exp.append(exp)

        return answer, answer_exp


    def factorize(self, polynomial: list[str], is_x: bool, return_native = False):
        GF2 = galois.GF(2)
        powers = [p[0] if is_x else p[1] for p in self.construct_powers_from_expression(polynomial)]

        # Construct the polynomial expression for galois
        expression = [1 if i in powers else 0 for i in range(self.l if is_x else self.m, -1, -1)]
        factors = galois.Poly(expression, field=GF2).factors()

        if return_native:
            return factors
        else:
            return self.galois_factors_to_expression(factors[0], factors[1], is_x)


    def raise_polynomial_to_power(self, polynomial: list[str], power: int):
        answer = ["i"]
        for _ in range(power):
            answer = self.multiply_polynomials(answer, polynomial)
        return answer


    def factorize_bivariate(self,P):
        P = self.construct_powers_from_expression(P)
        P_str = json.dumps(P)
        l_str = str(self.l)
        m_str = str(self.m)
        try:

            result = subprocess.run(['sage', '-python', 'factor_bivariate.py', P_str, l_str, m_str], capture_output=True,
                                    text=True, check=True)
            return result.stdout.strip()
        except Exception as e:
            print(f"Error running script: {e}")
