from ldpc.mod2 import nullspace, row_echelon, reduced_row_echelon, rank, row_span, row_basis

def are_matrices_equal(matrix1, matrix2, tolerance=1e-8):
    # Use numpy's allclose function to check element-wise equality with tolerance
    return np.allclose(matrix1, matrix2, atol=tolerance)

def is_dot_product_mod2_zero(matrix1, matrix2, tolerance=1e-8):
    # Check if the dot product results in the zero matrix
    result = matrix1 @ matrix2
    result_mod2 = np.mod(result,2)
    zero_matrix = np.zeros_like(result_mod2)
    return np.allclose(result_mod2, zero_matrix,atol=tolerance)

def is_gB_sum_hA_zero(A,B,g,h,tolerance=1e-8):
    gB = np.mod(g@B,2)
    hA = np.mod(h@A,2)
    gB_sum_hA = np.mod(gB+hA,2)
    zero_matrix = np.zeros_like(gB_sum_hA)
    return np.allclose(gB_sum_hA, zero_matrix,atol=tolerance)

def min_hamming_weight_of_matrix(matrix):
    """
    Finds the minimum Hamming weight among the rows of a matrix.

    Parameters:
    - matrix: NumPy array, the input matrix.
    
    Returns:
    - min_weight: int, the minimum Hamming weight.
    """

    # Ensure the matrix consists of binary elements
    if np.any((matrix != 0) & (matrix != 1)):
        raise ValueError("Matrix must contain only binary elements (0 or 1).")

    # Calculate Hamming weight for each row
    hamming_weights = np.sum(matrix, axis=1)

    # Find the minimum Hamming weight\
    min_weight = np.min(hamming_weights)

    return min_weight

def is_identity_matrix(matrix):
    # Check if the matrix is square
    if not matrix.shape[0] == matrix.shape[1]:
        return False
    
    # Check if all main diagonal elements are 1 and others are 0
    return np.all(np.eye(matrix.shape[0]) == matrix)

# row echelon 
import numpy as np
from scipy import sparse

def row_echelon_HS(matrix, full=False):
    
    """
    Converts a binary matrix to row echelon form via Gaussian Elimination

    Parameters
    ----------
    matrix : numpy.ndarry or scipy.sparse
        A binary matrix in either numpy.ndarray format or scipy.sparse
    full: bool, optional
        If set to `True', Gaussian elimination is only performed on the rows below
        the pivot. If set to `False' Gaussian eliminatin is performed on rows above
        and below the pivot. 
    
    Returns
    -------
        row_ech_form: numpy.ndarray
            The row echelon form of input matrix
        rank: int
            The rank of the matrix
        transform_matrix: numpy.ndarray
            The transformation matrix such that (transform_matrix@matrix)=row_ech_form
        pivot_cols: list
            List of the indices of pivot num_cols found during Gaussian elimination

    Examples
    --------
    >>> H=np.array([[1, 1, 1],[1, 1, 1],[0, 1, 0]])
    >>> re_matrix=row_echelon(H)[0]
    >>> print(re_matrix)
    [[1 1 1]
     [0 1 0]
     [0 0 0]]

    >>> re_matrix=row_echelon(H,full=True)[0]
    >>> print(re_matrix)
    [[1 0 1]
     [0 1 0]
     [0 0 0]]

    """
    num_rows, num_cols = np.shape(matrix)
    
    # Take copy of matrix if numpy (why?) and initialise transform matrix to identity
    if isinstance(matrix, np.ndarray):
        the_matrix = np.copy(matrix)
        transform_matrix = np.identity(num_rows).astype(int)
    elif isinstance(matrix, sparse.csr.csr_matrix):
        the_matrix = matrix
        transform_matrix = sparse.eye(num_rows, dtype="int", format="csr")
    else:
        raise ValueError('Unrecognised matrix type')

    pivot_row = 0
    pivot_cols = []

    reverse_quantum_circuit = []
    
    # Iterate over cols, for each col find a pivot (if it exists)
    for col in range(num_cols):

        # Select the pivot - if not in this row, swap rows to bring a 1 to this row, if possible
        if the_matrix[pivot_row, col] != 1:

            # Find a row with a 1 in this col
            swap_row_index = pivot_row + np.argmax(the_matrix[pivot_row:num_rows, col])

            # If an appropriate row is found, swap it with the pivot. Otherwise, all zeroes - will loop to next col
            if the_matrix[swap_row_index, col] == 1:

                # Swap rows
                the_matrix[[swap_row_index, pivot_row]] = the_matrix[[pivot_row, swap_row_index]]
                reverse_quantum_circuit.append('SWAP{}{}'.format(swap_row_index,pivot_row))
                # Transformation matrix update to reflect this row swap
                transform_matrix[[swap_row_index, pivot_row]] = transform_matrix[[pivot_row, swap_row_index]]

        # If we have got a pivot, now let's ensure values below that pivot are zeros
        if the_matrix[pivot_row, col]:

            if not full:  
                elimination_range = [k for k in range(pivot_row + 1, num_rows)]
            else:
                elimination_range = [k for k in range(num_rows) if k != pivot_row]

            # Let's zero those values below the pivot by adding our current row to their row
            for j in elimination_range:

                if the_matrix[j, col] != 0 and pivot_row != j:    ### Do we need second condition?

                    the_matrix[j] = (the_matrix[j] + the_matrix[pivot_row]) % 2
                    reverse_quantum_circuit.append('CX{}{}'.format(pivot_row,j)) # control is pivot row
                    # Update transformation matrix to reflect this op
                    transform_matrix[j] = (transform_matrix[j] + transform_matrix[pivot_row]) % 2

            pivot_row += 1
            pivot_cols.append(col)

        # Exit loop once there are no more rows to search
        if pivot_row >= num_rows:
            break

    # The rank is equal to the maximum pivot index
    matrix_rank = pivot_row
    row_esch_matrix = the_matrix

    return [row_esch_matrix, matrix_rank, transform_matrix, pivot_cols, reverse_quantum_circuit]


# def reduced_row_echelon_HS(matrix):
#     """
#     Converts matrix to reduced row echelon form such that the output has
#     the form rre=[I,A]

#     Parameters
#     ----------
#     matrix: numpy.ndarray
#         A binary matrix in numpy.ndarray format

#     Returns
#     -------
#     reduced_row_echelon_from: numpy.ndarray
#         The reduced row echelon form of the inputted matrix in the form rre=[I,A]
#     matrix_rank: int
#         The binary rank of the matrix
#     transform_matrix_rows: numpy.ndarray
#         The transformation matrix for row permutations
#     transform_matrix_cols: numpy.ndarray
#         The transformation matrix for the columns

#     Examples
#     --------
#     >>> H=np.array([[0, 0, 0, 1, 1, 1, 1],[0, 1, 1, 0, 0, 1, 1],[1, 0, 1, 0, 1, 0, 1]])
#     >>> rre=reduced_row_echelon(H)[0]
#     >>> print(rre)
#     [[1 0 0 1 1 0 1]
#      [0 1 0 1 0 1 1]
#      [0 0 1 0 1 1 1]]

#     """

#     num_rows, num_cols = matrix.shape
#     # print('OG MATRIX',matrix)
#     # Row reduce matrix to calculate rank and find the pivot cols
#     _, matrix_rank, _, pivot_columns, SWAP_indices_RE, CNOT_indices_RE = row_echelon_HS(matrix)

#     # Rearrange matrix so that the pivot columns are first
#     info_set_order = pivot_columns + [j for j in range(num_cols) if j not in pivot_columns]
#     print('ORDER',info_set_order)
#     transform_matrix_columns = (np.identity(num_cols)[info_set_order].astype(int)).T
#     # print('AM',matrix)
#     m_q = matrix @ transform_matrix_columns  # Rearranged M
#     print('m_q')
#     print(m_q)
#     # Row reduce m_q
#     reduced_row_echelon_form, _, transform_matrix_rows, _, SWAP_indices_RRE, CNOT_indices_RRE = row_echelon_HS(m_q, full=True)

#     return [reduced_row_echelon_form, matrix_rank, transform_matrix_rows, transform_matrix_columns, SWAP_indices_RE+CNOT_indices_RE+SWAP_indices_RRE+CNOT_indices_RRE]
