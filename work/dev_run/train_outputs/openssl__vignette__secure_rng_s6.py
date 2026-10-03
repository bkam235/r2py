import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# openssl is imported via the logic below

# No-op in Python

# r2py:entity:x
def rand_bytes(n=1):
    """Equivalent to openssl::rand_bytes using os.urandom for secure randomness."""
    return os.urandom(n)

def rand_num(n=1):
    """
    Translates the R rand_num logic:
    x <- matrix(as.numeric(rand_bytes(n * 8)), ncol = 8)
    as.numeric(x %*% 256^-(1:8))
    """
    # Generate n*8 bytes
    raw_bytes = rand_bytes(n * 8)
    # Convert to numeric array and reshape to (n, 8)
    # R's as.numeric on raw bytes gives 0-255
    x_mat = np.frombuffer(raw_bytes, dtype=np.uint8).reshape(n, 8).astype(float)
    
    # Weights: 256^-1, 256^-2, ..., 256^-8
    weights = 256.0**-np.arange(1, 9)
    
    # Matrix multiplication: each row of x_mat dot weights
    return x_mat.dot(weights)

# Secure rnorm: x <- qnorm(rand_num(1000), mean = 100, sd = 15)
u = rand_num(1000)
x = norm.ppf(u, loc=100, scale=15)

# hist(x)
# r2py:entity:hist
plt.hist(x, edgecolor='black', color='lightgray')
plt.show()