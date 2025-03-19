"""
Example usage of qec-bb package.
"""

from src import BBCode, BBCodeOptimised
from src.helpers import ProposeParameters

def basic_example():
    # Create a new BBCode
    l = 8
    m = 10
    A = ['i', 'x1', 'y7', 'x6.y5']
    B = ['x0', 'x5', 'y6.x7', 'x.y5']

    code = BBCode(l, m, A, B)

    # Find the parameters of the code
    # distance_method = 4 uses bposd to calculate the distance (recommended)
    n, k, d = code.generate_bb_code(distance_method=4)
    print(f"Code parameters: [{n}, {k}, {d}]")

    # Get parity-check matrices
    H_x, H_z = code.create_parity_check_matrices()
    print(f"H_x shape: {H_x.shape}, H_z shape: {H_z.shape}")

    # Create Tanner Graph
    G = code.make_graph()
    print(f"Tanner Graph - Number of nodes: {len(G.graph.nodes)}")
    print(f"Tanner Graph - Number of edges: {len(G.graph.edges)}")


def optimized_example():
    # Set up parameters
    l = 10
    m = 8
    num_codes = 5  # Generate 5 codes

    # Create an instance of BBCodeOptimised
    code = BBCodeOptimised(l, m)

    # Help generate random A and B expressions
    parameters = ProposeParameters(l, m)

    # Generate codes
    print("\nGenerating multiple codes with optimized implementation:")
    for i in range(num_codes):
        A = parameters.draw_bivariate_monomials(num_monomials=3)
        B = parameters.draw_bivariate_monomials(num_monomials=3)
        
        print(f"\nCode {i+1}:")
        print(f"A = {A}")
        print(f"B = {B}")
        
        code.set_expressions(A_expression=A, B_expression=B)
        n, k, d = code.generate_bb_code(distance_method=4)
        
        print(f"Code parameters: [{n}, {k}, {d}]")


if __name__ == "__main__":
    print("Basic BBCode example:")
    basic_example()
    
    print("\n" + "-"*50)
    
    optimized_example() 