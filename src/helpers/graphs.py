import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum

class Category(Enum):
    X = "x"
    Z = "z"
    L = "l"
    R = "r"


class PolynomialHandler:
    def __init__(self, l: int, m: int, graph: nx.Graph = None):
        self.l = l
        self.m = m
        self.graph = graph

    def construct_expression(self, x_power: int, y_power: int):
        x_power = x_power % self.l
        y_power = y_power % self.m

        if x_power == 0 and y_power == 0:
            return "i"
        if x_power == 0:
            return f"y{y_power}"
        if y_power == 0:
            return f"x{x_power}"
        return f"x{x_power}.y{y_power}"

    def construct_powers(self, monomial: str):
        x_power = 0
        y_power = 0
        for mu in monomial.split("."):
            if mu[0] == "x":
                x_power += int(mu[1:]) if len(mu) > 1 else 1
            if mu[0] == "y":
                y_power += int(mu[1:]) if len(mu) > 1 else 1
        return x_power % self.l, y_power % self.m

    def find_connector_monomial(self, base_label: str, check_label: str, T : bool):
        x1, y1 = self.construct_powers(base_label)
        x2, y2 = self.construct_powers(check_label)
        if T:
            return self.construct_expression(x1 - x2, y1 - y2)
        else:
            return self.construct_expression(x2 - x1, y2 - y1)

    def find_check_labels(self, base_node):
        x_check_labels = []
        z_check_labels = []
        for e in self.graph.edges:
            if e[0] == base_node:
                if self.graph.nodes[e[1]]["category"] == Category.X:
                    x_check_labels.append(self.graph.nodes[e[1]]["label"])
                else:
                    z_check_labels.append(self.graph.nodes[e[1]]["label"])
            if e[1] == base_node:
                if self.graph.nodes[e[0]]["category"] == Category.X:
                    x_check_labels.append(self.graph.nodes[e[0]]["label"])
                else:
                    z_check_labels.append(self.graph.nodes[e[0]]["label"])
        return x_check_labels, z_check_labels


class TannerGraph:
    def __init__(self, Hx: np.ndarray, Hz: np.ndarray):
        self.Hx = Hx
        self.Hz = Hz
        self.validate_input()
        self.graph = nx.Graph()
        self.l = 0
        self.m = 0

    def set_l_and_m(self, l: int, m: int):
        self.l = l
        self.m = m
        return self

    def validate_input(self):
        if self.Hx.shape != self.Hz.shape:
            raise ValueError("Hx and Hz must have the same shape")

    def _generate_labels(self):
        if self.l == 0 or self.m == 0:
            raise ValueError("l and m must be set before generating monomial labels")

        labels = []
        poly_help = PolynomialHandler(self.l, self.m)
        for i in range(self.l):
            for j in range(self.m):
                labels.append(poly_help.construct_expression(i, j))
        return labels

    def _add_edges(self, hx, hz, dl, dr):
        m, n = self.Hx.shape
        for i in range(m):
            for j in range(n):
                # add x checks
                if self.Hx[i][j] != 0:
                    node = dl[j] if j < n // 2 else dr[j - n // 2]
                    self.graph.add_edge(hx[i], node)
                # add z checks
                if self.Hz[i][j] != 0:
                    node = dl[j] if j < n // 2 else dr[j - n // 2]
                    self.graph.add_edge(hz[i], node)

    def _add_nodes(self, hx, hz, dl, dr, labels):
        for i, label in enumerate(labels):
            self.graph.add_node(hx[i], label=label, category=Category.X)
            self.graph.add_node(hz[i], label=label, category=Category.Z)
            self.graph.add_node(dl[i], label=label, category=Category.L)
            self.graph.add_node(dr[i], label=label, category=Category.R)

    def add_nodes_and_edges(self):
        num_checks, num_bits = self.Hx.shape

        # bbcode naming convention
        hx = [f"x{i}" for i in range(num_checks)]
        hz = [f"z{i}" for i in range(num_checks)]
        dl = [f"l{i}" for i in range(num_checks)]
        dr = [f"r{i}" for i in range(num_checks)]

        labels = self._generate_labels()
        self._add_nodes(hx, hz, dl, dr, labels)
        self._add_edges(hx, hz, dl, dr)

    def is_connected(self):
        return nx.is_connected(self.graph)

    def num_connected_components(self):
        return nx.number_connected_components(self.graph)

    def plot_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold')
        plt.show()

    def deconstruct_polynomials(self, base_node: str = "l0"):
        # l connected to x and z via aT and b
        # r connected to x and z via bT and a

        if base_node not in self.graph.nodes:
            raise Exception("Base node not found in graph")

        base_label = self.graph.nodes[base_node]["label"]
        poly_help = PolynomialHandler(self.l, self.m, self.graph)

        x_check_labels, z_check_labels = poly_help.find_check_labels(base_node)
        a_expression = [poly_help.find_connector_monomial(base_label, x, True) for x in x_check_labels]
        b_expression = [poly_help.find_connector_monomial(base_label, z, False) for z in z_check_labels]

        return a_expression, b_expression
