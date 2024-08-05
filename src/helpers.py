import networkx as nx
import numpy as np
from ldpc.mod2 import reduced_row_echelon, rank
from copy import deepcopy

from matplotlib import pyplot as plt


## ----------------- QEC Specific Helpers ----------------- ##


def generators(G_standard):
    G1=G_standard[:][:G_standard.shape[1]//2]
    G2=G_standard[:][G_standard.shape[1]//2:]
    H_x = G1[ ~ np.all(G1 == 0, axis=1)]
    H_z = G2[ ~ np.all(G2 == 0, axis=1)]
    return H_x, H_z


def standard_form(H_x, H_z):
    G = make_block_diagonal(H_x, H_z)
    n, m = G.shape[1] // 2, G.shape[0]

    G1 = G[:, :n]
    G2 = G[:, n:]
    G1_rref, r, G1_transform_rows, G1_transform_cols = reduced_row_echelon(G1)
    G2 = (G1_transform_rows@G2@G1_transform_cols)%2

    E = G2[r:,r:]
    E_rref, s, E_transform_rows, E_transform_cols = reduced_row_echelon(E)
    D = ( E_transform_rows @ G2[r:,:r] ) % 2
    C = ( G2[:r,r:] @ E_transform_cols ) % 2

    A = ( G1_rref[:r,r:] @ E_transform_cols ) % 2

    G1_rref[:r,r:] = A
    G2[r:,r:] = E_rref
    G2[r:,:r] = D
    G2[:r,r:] = C

    G_complete = np.hstack((G1_rref, G2))
    G_standard = G_complete[ ~ np.all(G_complete == 0, axis=1)]
    return G_standard


def find_logical_generators(G_standard, rank_x: int) -> list[np.ndarray]:
    n = G_standard.shape[1] // 2
    k = n - G_standard.shape[0]

    A2 = deepcopy(G_standard[: rank_x, n - k: n])
    E  = deepcopy(G_standard[rank_x:, n + n - k:])
    C  = deepcopy(G_standard[: rank_x, n + n - k:])

    zero_l = np.zeros((k, rank_x), dtype=int)
    zero_m = np.zeros((k, n - k - rank_x), dtype=int)
    zero_r = np.zeros((k, k), dtype=int)

    identity = np.eye(k)

    Lx = np.hstack((zero_l, E.T, identity, C.T, zero_m, zero_r))
    Lz = np.hstack((zero_l, zero_m, zero_r, A2.T, zero_m, identity))

    return Lx, Lz


## ----------------- Linear Algebra Helpers ----------------- ##


def display(M, middle_line = False):
    size = len(M[0])

    h_line = "--" * size
    print(h_line)

    for row in M:
        print("[ ", end = "")
        for i in range(size):
            print(row[i], end = " ")
            if middle_line and i == size / 2:
                print("|", end = " ")
        print("]")

    print(h_line)
    pass


def hamming_weight(vector: list[int]):
    # hamming weight for a CSS src logical operator (length = 2n)
    n = len(vector) // 2
    weight = sum([1 if vector[i] == 1 or vector[i + n] == 1 else 0 for i in range(n)])
    return weight


def make_block_diagonal(H_x, H_z):
    G = np.block([
        [H_x, np.zeros((H_x.shape[0], H_z.shape[1]), dtype=int)],
        [np.zeros((H_z.shape[0], H_x.shape[1]), dtype=int), H_z]
    ])
    return G


def create_matrix_S(size):
    S = np.eye(size, dtype=int, k=1)
    S[size - 1][0] = 1
    return S


def binary_rank(A):
    return rank(A)


## ----------------- Miscellaneous ----------------- ##

def plot_graph(G : nx.Graph, hx : list[str], hz : list[str], d : list[str]):
    pos = {}
    pos_hx = {}
    x = 0.100
    const = 0.100
    y = 1.0

    for i in range(len(hx)):
        pos_hx[hx[i]] = [x, y - i * const]

    xb = 0.900
    pos_hz = {}
    for i in range(len(hz)):
        pos_hz[hz[i]] = [xb, y - i * const]

    xd = 0.500
    pos_d = {}
    for i in range(len(d)):
        pos_d[d[i]] = [xd, y - i * const]


    nx.draw_networkx_nodes(G, pos_hx, nodelist=hx, node_color='r', node_size=300, alpha=0.8)
    nx.draw_networkx_nodes(G, pos_hz, nodelist=hz, node_color='b', node_size=300, alpha=0.8)
    nx.draw_networkx_nodes(G, pos_d, nodelist=d, node_color='g', node_size=300, alpha=0.8)
    pos.update(pos_hx)
    pos.update(pos_hz)
    pos.update(pos_d)
    nx.draw_networkx_edges(G,pos,edgelist=nx.edges(G),width=1,alpha=0.8,edge_color='k')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    plt.show()



def compute_sub_graphs(G: nx.Graph):
    A = [G.subgraph(c) for c in nx.connected_components(G)]
    print(f"Number of connected components: {len(A)}")
    return A



def make_graph(Hx: np.ndarray, Hz: np.ndarray, plot=True):
    G = nx.Graph()

    hx = ['X' + str(i) for i in range(len(Hx))]
    hz = ['Z' + str(j) for j in range(len(Hz))]
    d = [str(k) for k in range(len(Hx[0]))]
    G.add_nodes_from(hx, bipartite=0)
    G.add_nodes_from(hz, bipartite=1)
    G.add_nodes_from(d, bipartite=2)

    for i in range(len(Hx)):
        for j in range(len(Hx[i])):
            if Hx[i][j] != 0:
                G.add_edge(hx[i], d[j])

    for i in range(len(Hz)):
        for j in range(len(Hz[i])):
            if Hz[i][j] != 0:
                G.add_edge(hz[i], d[j])

    if plot:
        plot_graph(G, hx, hz, d)

    return G


