# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: list_unchop.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 24

suppressPackageStartupMessages(library(vctrs))
# If `indices` selects every value in `x` exactly once,
# in any order, then `list_unchop()` inverts `vec_chop()`
x <- c("a", "b", "c", "d")
indices <- list(2, c(3, 1), 4)
vec_chop(x, indices = indices)
list_unchop(vec_chop(x, indices = indices), indices = indices)

# When unchopping, size 1 elements of `x` are recycled
# to the size of the corresponding index
list_unchop(list(1, 2:3), indices = list(c(1, 3, 5), c(2, 4)))

# Names are retained, and outer names can be combined with inner
# names through the use of a `name_spec`
lst <- list(x = c(a = 1, b = 2), y = 1)
list_unchop(lst, indices = list(c(3, 2), c(1, 4)), name_spec = "{outer}_{inner}")

# If you have a list of homogeneous vectors, sometimes it can be useful to
# unchop, apply a function to the flattened vector, and then rechop according
# to the original indices. This can be done efficiently with `list_sizes()`.
x <- list(c(1, 2, 1), c(3, 1), 5, double())
x_flat <- list_unchop(x)
x_flat <- x_flat + max(x_flat)
vec_chop(x_flat, sizes = list_sizes(x))