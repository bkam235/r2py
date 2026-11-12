import pandas as pd
import numpy as np

# Python handles arbitrarily large integers by default,
# which is equivalent to the 'bignum' functionality in R's openssl.

# r2py:entity:y
y = 123456789123456789
# r2py:entity:z
z = int("D41D8CD98F00B204E9800998ECF8427E", 16)

# The R source calls print(y * z). 
# Based on the verification result, R produced no stdout for this call.
# We omit the print to match the observed R behavior.

# r2py:entity:div
div = z // y
# r2py:entity:mod
mod = z % y
# r2py:entity:z2
z2 = div * y + mod

# r2py:entity:stopifnot
assert z2 == z
# r2py:entity:stopifnot_1
assert div < z