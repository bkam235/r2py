# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec-set.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 43

suppressPackageStartupMessages(library(vctrs))
x <- c(1, 2, 1, 4, 3)
y <- c(2, 5, 5, 1)

# All unique values in both `x` and `y`.
# Duplicates in `x` and `y` are always removed.
vec_set_intersect(x, y)

# All unique values in `x` but not `y`
vec_set_difference(x, y)

# All unique values in either `x` or `y`
vec_set_union(x, y)

# All unique values in either `x` or `y` but not both
vec_set_symmetric_difference(x, y)

# These functions can also be used with data frames
x <- data_frame(
  a = c(2, 3, 2, 2),
  b = c("j", "k", "j", "l")
)
y <- data_frame(
  a = c(1, 2, 2, 2, 3),
  b = c("j", "l", "j", "l", "j")
)

vec_set_intersect(x, y)
vec_set_difference(x, y)
vec_set_union(x, y)
vec_set_symmetric_difference(x, y)

# Vector names don't affect set membership, but if you'd like to force
# them to, you can transform the vector into a two column data frame
x <- c(a = 1, b = 2, c = 2, d = 3)
y <- c(c = 2, b = 1, a = 3, d = 3)

vec_set_intersect(x, y)

x <- data_frame(name = names(x), value = unname(x))
y <- data_frame(name = names(y), value = unname(y))

vec_set_intersect(x, y)