# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: list_assign.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 25

suppressPackageStartupMessages(library(purrr))
x <- list(x = 1:10, y = 4, z = list(a = 1, b = 2))
str(x)

# Update values
str(list_assign(x, a = 1))

# Replace values
str(list_assign(x, z = 5))
str(list_assign(x, z = NULL))
str(list_assign(x, z = list(a = 1:5)))

# Replace recursively with list_modify(), leaving the other elements of z alone
str(list_modify(x, z = list(a = 1:5)))

# Remove values
str(list_assign(x, z = zap()))

# Combine values with list_merge()
str(list_merge(x, x = 11, z = list(a = 2:5, c = 3)))

# All these functions support dynamic dots features. Use !!! to splice
# a list of arguments:
l <- list(new = 1, y = zap(), z = 5)
str(list_assign(x, !!!l))