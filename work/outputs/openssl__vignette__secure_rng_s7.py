# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 4

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# r2py:entity:y
def rand_num(n=1):
    """
    Mimics R openssl::rand_num.
    Generates n random floats in [0, 1) using cryptographically secure bytes.
    """
    # To be as close as possible to R's openssl::rand_num, 
    # we generate random bytes and convert to float in [0, 1).
    res = []
    for _ in range(n):
        # Use 8 bytes for 64-bit precision
        b = os.urandom(8)
        val_int = int.from_bytes(b, byteorder='big')
        # Normalize to [0, 1)
        res.append(val_int / 2**64)
    return np.array(res)

# Secure rbinom equivalent
# y <- qbinom(rand_num(1000), size = 20, prob = 0.1)
random_probs = rand_num(1000)
# qbinom is the quantile function (ppf in scipy)
y = binom.ppf(random_probs, 20, 0.1).astype(int)

# hist(y, breaks = -.5:(max(y)+1))
# R's -.5:(max(y)+1) produces a sequence starting at -0.5 with step 1.
# The end point is max(y)+1. In numpy.arange, the stop value is exclusive.
# To include max(y)+1, we use max(y)+1.5.
# r2py:entity:hist
bins = np.arange(-0.5, np.max(y) + 1.5, 1)

plt.figure()
plt.hist(y, bins=bins, edgecolor='black', color='lightgray')
plt.show()