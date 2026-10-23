# Translated from <R script> by r2py v0.3.0

# Python handles arbitrarily large integers by default,
# which is equivalent to the 'bignum' functionality in R's openssl.

# r2py:entity:y
y = 123456789123456789
# r2py:entity:z
z = int("D41D8CD98F00B204E9800998ECF8427E", 16)

# R's openssl::bignum print method may not produce standard stdout in this environment,
# but for execution equivalence, we perform the multiplication.
# r2py:entity:print
_ = y * z

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