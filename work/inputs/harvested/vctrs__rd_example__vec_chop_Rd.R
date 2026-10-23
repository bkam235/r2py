# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_chop.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 25

suppressPackageStartupMessages(library(vctrs))
vec_chop(1:5)

# These two are equivalent
vec_chop(1:5, indices = list(1:2, 3:5))
vec_chop(1:5, sizes = c(2, 3))

# Can also be used on data frames
vec_chop(mtcars, indices = list(1:3, 4:6))

# If you know your input is sorted and you'd like to split on the groups,
# `vec_run_sizes()` can be efficiently combined with `sizes`
df <- data_frame(
  g = c(2, 5, 5, 6, 6, 6, 6, 8, 9, 9),
  x = 1:10
)
vec_chop(df, sizes = vec_run_sizes(df$g))

# If you have a list of homogeneous vectors, sometimes it can be useful to
# combine, apply a function to the flattened vector, and chop according
# to the original indices. This can be done efficiently with `list_sizes()`.
x <- list(c(1, 2, 1), c(3, 1), 5, double())
x_flat <- vec_c(!!!x)
x_flat <- x_flat + max(x_flat)
vec_chop(x_flat, sizes = list_sizes(x))