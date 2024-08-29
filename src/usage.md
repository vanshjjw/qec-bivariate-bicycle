
# BBCode Class

Code for the `BBCode` class can be found in `src\core.py`.

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


-----------------------------------

# BBCodeOptimised Class

Code for the `BBCodeOptimised` class can be found in `src\core_optimised.py`.

This class is similar to the `BBCode` class but is more efficient for generating multiple codes with the same `l` and `m`. It caches the values of `x` and `y` in the polynomial ring.

Example usage:

```python

from src.helpers.parameters import ProposeParameters
from src.core_optimised import BBCodeOptimised

# generate 10 different codes with the same l and m
l = 10
m = 8
num_codes = 50

# create an instance of BBCodeOptimised. Only set l and m once
code = BBCodeOptimised(l, m)

# Help generate random A and B expressions
# See `src\helpers\parameters.py` for more information
parameters = ProposeParameters(l, m)


# generate codes
codes = []
for _ in range(num_codes):
    # generate random A and B expressions using some method. 
    # The variables x and y have the l and m for all iterations.
    A = parameters.draw_bivariate_monomials(num_monomials=3)
    B = parameters.draw_bivariate_monomials(num_monomials=3)
    
    # generate code
    code.set_expressions(A_expression=A, B_expression=B)
    n, k, d = code.find_distance(distance_method=3)
    
    # analysis for the polynomials and the code parameters
    ...
    ...
    
# For roughly for l, m < 50, and number of codes > 20, BBCodeOptimised works 2-3X faster than BBCode
```

-----------------------------------

# GeneralGroupAlgebraCodes Class

Code for the `GeneralGroupAlgebraCodes` class can be found in `src\core_generalised.py`.

Documentation to be added. Look at `tests\codes\bbcode_generalised.py` for input and usage examples.


