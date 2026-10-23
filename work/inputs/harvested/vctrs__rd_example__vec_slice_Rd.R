# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_slice.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 71

suppressPackageStartupMessages(library(vctrs))
x <- sample(10)
x
vec_slice(x, 1:3)

# You can assign with the infix variant:
vec_slice(x, 2) <- 100
x

# Or with the regular variant that doesn't modify the original input:
y <- vec_assign(x, 3, 500)
y
x


# Slicing objects of higher dimension:
vec_slice(mtcars, 1:3)

# Type stability --------------------------------------------------

# The assign variant is type stable. It always returns the same
# type as the input.
x <- 1:5
vec_slice(x, 2) <- 20.0

# `x` is still an integer vector because the RHS was cast to the
# type of the LHS:
vec_ptype(x)

# Compare to `[<-`:
x[2] <- 20.0
vec_ptype(x)


# Note that the types must be coercible for the cast to happen.
# For instance, you can cast a double vector of whole numbers to an
# integer vector:
vec_cast(1, integer())

# But not fractional doubles:
try(vec_cast(1.5, integer()))

# For this reason you can't assign fractional values in an integer
# vector:
x <- 1:3
try(vec_slice(x, 2) <- 1.5)

# Slicing `value` -------------------------------------------------

# Sometimes both `x` and `value` start from objects that are the same length,
# and you need to slice `value` by `i` before assigning it to `x`. This comes
# up when thinking about how `base::ifelse()` and `dplyr::case_when()` work.
condition <- c(TRUE, FALSE, TRUE, FALSE)
yes <- 1:4
no <- 5:8

# Create an output container and fill it
out <- vec_init(integer(), 4)
out <- vec_assign(out, condition, vec_slice(yes, condition))
out <- vec_assign(out, !condition, vec_slice(no, !condition))
out

# This is wasteful because you have to materialize the slices of `yes` and
# `no` before they can be assigned, and you also have to validate `condition`
# multiple times. Using `slice_value` internally performs
# `vec_slice(yes, condition)` and `vec_slice(no, !condition)` for you,
# but does so in a way that avoids the materialization.
out <- vec_init(integer(), 4)
out <- vec_assign(out, condition, yes, slice_value = TRUE)
out <- vec_assign(out, !condition, no, slice_value = TRUE)
out