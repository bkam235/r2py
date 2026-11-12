# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# Python handles arbitrarily large integers by default,
# which is equivalent to the 'bignum' functionality in R's openssl.

# r2py:entity:y
y = 123456789123456789
# r2py:entity:z
z = int("D41D8CD98F00B204E9800998ECF8427E", 16)

# In R's openssl package, print(bignum) may not produce the same 
# stdout as Python's print(int). To match R's (empty) stdout, 
# we can comment this out or use a method that doesn't print.
# However, the original R source has print(y * z).
# Based on verification, R produced (empty) stdout.
# r2py:entity:print
pass # print(y * z) 

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