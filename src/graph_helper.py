import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class TannerGraph:
    def __init__(self, Hx: np.ndarray, Hz: np.ndarray):
        self.Hx = Hx
        self.Hz = Hz
        self.validate_input()
        self.graph = nx.Graph()


    def validate_input(self):
        if self.Hx.shape != self.Hz.shape:
            raise ValueError("Hx and Hz must have the same shape")


    def make_graph(self):
        m, n = self.Hx.shape

        hx = ['x' + str(i) for i in range(m)]
        hz = ['z' + str(i) for i in range(m)]
        data = [str(i) for i in range(n)]

        self.graph.add_nodes_from(hx, is_x_check = True)
        self.graph.add_nodes_from(hz, is_z_check = True)
        self.graph.add_nodes_from(data, is_qubit = True)

        for i in range(m):
            for j in range(n):
                if self.Hx[i][j] != 0:
                    self.graph.add_edge(hx[i], data[j])
                if self.Hz[i][j] != 0:
                    self.graph.add_edge(hz[i], data[j])


    def is_connected(self):
        return nx.is_connected(self.graph)


    def num_connected_components(self):
        return nx.number_connected_components(self.graph)


    def plot_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold')
        plt.show()

