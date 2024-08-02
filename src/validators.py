import numpy as np

def validate_parity_matrix(H_x, H_z):
    # check matrices are binary
    assert np.array_equal(H_x, H_x % 2)
    assert np.array_equal(H_z, H_z % 2)

    # check commutativity condition
    M = (H_x @ H_z.T) % 2
    for i in range(len(M)):
        for j in range(len(M[0])):
            assert np.isclose(M[i][j], 0), f"H_x @ H_z.T non-zero at index ({i}, {j}) with value {M[i][j]}"
    pass


def validate_standard_CSS(n, k, S_x, S_z, rank_x, rank_z):
    # check n - k stabilizer generators
    assert rank_x + rank_z == n - k
    assert S_x.shape == (rank_x, n)
    assert S_z.shape == (rank_z, n)
    
    # S_x has an r x r identity
    assert np.array_equal(S_x[:rank_x][:rank_x], np.eye(rank_x))

    # check if S_z has an n - k - rank_x = rank_z sized identity in the middle
    assert np.array_equal(S_z[:][rank_x : n - k], np.eye(rank_z))
    pass


def validate_x_y_matrices(x):
    # each row must have only one 1 and rest 0
    for row in x:
        assert sum(row) == 1, f"Row with sum {sum(row)} found in x matrix"
    pass


def validate_A_B_matrices(A, A_expression):
    # Number of 1's in each row is equal to the number of terms in A_expression
    weight = len(A_expression)
    for i, row in enumerate(A):
        assert sum(row) == weight, f"Row with weight {sum(row)} found in A matrix at index {i}"
    pass


def validate_ranks(rank_H_x, rank_H_z):
    assert rank_H_x == rank_H_z
    pass

