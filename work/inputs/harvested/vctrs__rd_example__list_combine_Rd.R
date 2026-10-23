# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: list_combine.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 64

suppressPackageStartupMessages(library(vctrs))
# Combine a list of vectors using
# a list of `indices`
x <- list(
  1:3,
  4:6,
  7:8
)
indices <- list(
  c(1, 3, 7),
  c(8, 6, 5),
  c(2, 4)
)
list_combine(x, indices = indices, size = 8)

# Overlapping `indices` are allowed.
# The last match "wins" by default.
x <- list(
  1:3,
  4:6
)
indices <- list(
  c(1, 2, 3),
  c(1, 2, 6)
)
list_combine(x, indices = indices, size = 6)

# Use `multiple` to force the first match to win.
# This is similar to how `dplyr::case_when()` works.
list_combine(x, indices = indices, size = 6, multiple = "first")

# Works with data frames as well.
# Now how index 2 is not assigned to.
x <- list(
  data.frame(x = 1:2, y = c("a", "b")),
  data.frame(x = 3:4, y = c("c", "d"))
)
indices <- list(
  c(4, 1),
  c(3, NA)
)
list_combine(x, indices = indices, size = 4)

# You can use `size` to combine into a larger object than you have values for
list_combine(list(1:2, 4:5), indices = list(1:2, 4:5), size = 8)

# Additionally specifying `default` allows you to control the value used in
# unfilled locations
list_combine(
  list(1:2, 4:5),
  indices = list(1:2, 4:5),
  size = 8,
  default = 0L
)

# Alternatively, if you'd like to assert that you've covered all output
# locations through `indices`, set `unmatched = "error"`.
# Here, we've set the size to 5 but missed location 3:
try(list_combine(
  list(1:2, 4:5),
  indices = list(1:2, 4:5),
  size = 5,
  unmatched = "error"
))