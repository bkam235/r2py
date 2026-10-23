# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: list_of_transpose.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 79

suppressPackageStartupMessages(library(vctrs))
# A form of `list_of()` that infers both ptype and size
list_of2 <- function(...) {
  list_of(..., .ptype = NULL, .size = NULL)
}

# I: list_of<integer[2]>[3]
# O: list_of<integer[3]>[2]
list_of_transpose(list_of2(1:2, 3:4, 5:6))

# With data frames
x <- data_frame(a = 1:2, b = letters[1:2])
y <- data_frame(a = 3:4, b = letters[3:4])
list_of_transpose(list_of2(x, y))

# Size 1 elements are recycled
list_of_transpose(list_of2(1, 2:3, 4))

# ---------------------------------------------------------------------------
# `NULL` handling

# `NULL` values aren't allowed in `list_of_transpose()`
x <- list_of2(1:3, NULL, 5:7, NULL)
try(list_of_transpose(x))

# Either drop them entirely or replace them up front before transposing

x_dropped <- vec_slice(x, !vec_detect_missing(x))
x_dropped

list_of_transpose(x_dropped)

x_replaced <- vec_assign(x, vec_detect_missing(x), list(NA))
x_replaced

list_of_transpose(x_replaced)

# ---------------------------------------------------------------------------
# Reversibility

# Because `list_of_transpose()` takes and returns fully specified list-ofs,
# it is fully reversible, even in the edge cases.
x <- list_of2(integer(), integer())

# This returns a list of size 0
# I: list_of<integer[0]>[2]
# O: list_of<integer[2]>[0]
out <- list_of_transpose(x)
out

# Even though there are no elements, we know the element size and type,
# so we can transpose a second time to recover `x`. This would not be
# possible if this function returned a bare `list()`, which would result
# in lost information.
# I: list_of<integer[2]>[0]
# O: list_of<integer[0]>[2]
list_of_transpose(out)

# ---------------------------------------------------------------------------
# Padding

# If you'd like to pad with a missing value rather than erroring,
# you might do something like this, which left-pads before conversion
# to list-of.
x <- list(1, 2:5, 6:7)

sizes <- list_sizes(x)
size <- max(sizes)
index <- which(sizes != size)

x[index] <- lapply(
  index,
  function(i) vec_c(rep(NA, times = size - sizes[[i]]), x[[i]])
)
x

x <- as_list_of(x, .ptype = NULL, .size = NULL)

list_of_transpose(x)