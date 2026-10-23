# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: list_of.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 53

suppressPackageStartupMessages(library(vctrs))
# Restrict the type, but not the size
x <- list_of(1:3, 5:6, 10:15)
x

if (requireNamespace("tibble", quietly = TRUE)) {
  # As a column in a tibble
  tibble::tibble(x = x)
}

# Coercion happens during assignment
x[1] <- list(4)
typeof(x[[1]])

try(x[1] <- list(4.5))

# Restrict the size, but not the type
x <- list_of(1, 2:3, .ptype = rlang::zap(), .size = 2)
x

# Recycling happens during assignment
x[1] <- list(4)
x

try(x[1] <- list(3:6))

# Restricting both size and type
x <- list_of(1L, 2:3, .ptype = integer(), .size = 2)
x

# Setting an element to `NULL`
x[2] <- list(NULL)
x

# Note that using `NULL` shortens the list, like a base R list
x[2] <- NULL
x

# Combining a list_of with a list results in a list
vec_c(list_of(1), list(2, "x"))

# Combining a list_of with another list_of tries to find a common element
# type and common element size, but will remove the constraint if that
# fails
x <- list_of(1, .ptype = double())
y <- list_of(c("a", "b"), .ptype = character(), .size = 2)
z <- list_of(c("c", "d", "e"), .ptype = character(), .size = 3)

# Falls back to a list
vec_c(x, y)

# Falls back to a `list_of<character>` with no size restriction
vec_c(y, z)