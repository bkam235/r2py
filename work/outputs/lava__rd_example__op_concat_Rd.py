import numpy as np
from scipy.linalg import block_diag

# The %++% operator in lava is a "compose" or "addition" operator 
# that handles different types of inputs (matrices, strings, functions).
# r2py:entity:matrix
def compose_op(a, b):
    if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
        # For matrices, lava's %++% performs block diagonal concatenation
        return block_diag(a, b)
    elif isinstance(a, str) and isinstance(b, str):
        return a + b
    elif callable(a) and callable(b):
        # Function composition: (f %++% g)(x) = f(g(x))
        return lambda x: a(b(x))
    else:
        return a + b

# Block diagonal
# matrix(rnorm(25),5)%++%matrix(rnorm(25),5)
# r2py:entity:matrix_1
mat1 = np.random.randn(5, 5)
mat2 = np.random.randn(5, 5)
res_mat = compose_op(mat1, mat2)
print(res_mat)

# String concatenation
# "Hello "%++%" World"
res_str = compose_op("Hello ", " World")
print(f'[1] "{res_str}"')

# Function composition
# f <- log %++% exp
# r2py:entity:f
f = compose_op(np.log, np.exp)

# f(2)
# r2py:entity:f_1
res_val = f(2)
# R prints result of log(exp(2)) as 2
print(f'[1] {int(round(res_val)) if np.isclose(res_val, round(res_val)) else res_val}')