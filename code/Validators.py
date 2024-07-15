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

def validate_standard_CSS(n, k, S_x, S_z, rank_S_x, rank_S_z):
    #check if there are n-k X and Z stabilizer generators
    assert S_x.shape == (rank_S_x, n) and S_z.shape == (n-k-rank_S_x, n)
    
    #check if S_x has (r x r) identity on the left
    I_x=np.eye(rank_S_x)
    assert np.array_equal(S_x[:rank_S_x][:rank_S_x], I_x)

    #check if S_z has (n-k-r x n-k-r) identity in the middle
    I_z=np.eye(n-k-rank_S_x)
    assert np.array_equal(S_z[:][rank_S_x:n-k],I_z)


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


def validate_rank(rank_H_x, rank_H_z):
    assert rank_H_x == rank_H_z
    pass

