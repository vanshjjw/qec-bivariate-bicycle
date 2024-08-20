import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


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

        labels = set()
        for i in range(self.l):
            for j in range(self.m):
                labels.add(f"x{i}y{j}")

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
            self.graph.add_node(hx[i], label=label, category="x")
            self.graph.add_node(hz[i], label=label, category="z")
            self.graph.add_node(dl[i], label=label, category="l")
            self.graph.add_node(dr[i], label=label, category="r")

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

