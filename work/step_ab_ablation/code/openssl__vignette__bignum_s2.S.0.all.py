# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:entity:import_openssl
# No direct Python equivalent for openssl::bignum needed as Python ints are arbitrary precision.
import pandas as pd
import numpy as np

# r2py:entity:suppressPackageStartupMessages
# This is a no-op in Python.

# r2py:entity:y
y = int("123456789123456789")
# r2py:entity:z
z = int("D41D8CD98F00B204E9800998ECF8427E", 16)

# r2py:entity:print
print(y * z)

# Basic arithmetic
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