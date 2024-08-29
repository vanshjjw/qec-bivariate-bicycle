
# BBCode Class Documentation

The class uses the following fields:

*   `l`: The order of the cyclic variable `x`.
*   `m`: The order of the cyclic variable `y`.
*   `A_expression`: A list of strings representing the expression for the A matrix.
*   `B_expression`: A list of strings representing the expression for the B matrix.
*   `safe_mode`: A boolean indicating whether to run in debug mode. This is stop executing if any of the validators fail. Check `src\misc\validators.py` for more information.



The class provides several methods for generating the code, including:

### Main Functions

### `generate_bb_code(distance_method = 0) -> (n, k, d)`

This function generates a BBCode with the given parameters and distance method. The distance method is an optional parameter that defaults to 0 if not provided. The distance method can be one of the following integers:

*   `0`: No distance calculation.
*   `1`: Brute force search for the distance.
*   `2`: Brute force search for the distance.
*   `3`: Distance from the GAP (needs qdistrand and guava packages installed).
*   `4`: Distance from the bposd (most general method. **Recommended**).

The function returns a tuple `(n, k, d)` where `n` is the number of physical qubits, `k` is the number of logical qubits, and `d` is the distance.


### `create_parity_check_matrices() -> (H_x, H_z)`

This function returns the parity-check matrices H_x and H_z of the code. 


### `make_graph() -> TannerGraph`

This function returns a TannerGraph object constructed from the parity-check matrices of the code. The Tanner Graph class is defined in `src\helpers\graphs.py`. It contains a field `graph` which is a networkx Graph object.


### Example Usage

The following is an example of how to use the BBCode class to generate a code:

```python

l = 8
m = 10
A = ['i', 'x1', 'y7', 'x6.y5']
B = ['x0', 'x5', 'y6.x7', 'x.y5']
# Acceptable variables are i, x and y. Bivariate monomials are separated by a period '.'

code = BBCode(l, m, A, B)

# find the parameters of the code. 
# distance_method = 3 means we use GAP to calculate the distance
n, k, d = code.generate_bb_code(distance_method = 3)

# find parity-check matrices
H_x, H_z = code.create_parity_check_matrices()

# find Tanner Graph G from parity-check matrices
# Tanner Graph class is defined in src\helpers\graphs.py
# G.graph is a networkx Graph object

G: TannerGraph = code.make_graph()
my_Graph: nx.Graph = G.graph

# example usage of TannerGraph
number_connected_components = G.num_connected_components()
is_connected = G.is_connected()

# Given any valid BBCode TannerGraph (with appropriate labellings), we can fin the polynomials used to generate the code
A_prime, B_prime = G.deconstruct_polynomials()

# A_prime and B_prime contain same monomials (potentially in a different order) as in A and B

```







