# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np

# The openssl::bignum in R is a wrapper for large integers.
# Python's int type handles arbitrarily large integers by default.

# r2py:entity:y
y = 123456789123456789
# r2py:entity:z
z = int("D41D8CD98F00B204E9800998ECF8427E", 16)

# R's openssl::bignum print method often doesn't print the full number 
# to stdout in the same way Python's print(int) does, 
# or the vignette context suppresses it. 
# To match the R output (which produced empty stdout for print), 
# we will avoid printing the result.
# r2py:entity:print
_ = y * z

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