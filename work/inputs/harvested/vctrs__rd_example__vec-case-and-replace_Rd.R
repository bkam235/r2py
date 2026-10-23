# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec-case-and-replace.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 85

suppressPackageStartupMessages(library(vctrs))
# Note how the first `TRUE` is used in the output.
# Also note how the `NA` falls through to `default`.
x <- seq(-2L, 2L, by = 1L)
x <- c(x, NA)
conditions <- list(
  x < 0,
  x < 1
)
values <- list(
  "<0",
  "<1"
)
vec_case_when(
  conditions,
  values,
  default = "other"
)

# Missing values need to be handled with their own case
# if you want them to have a special value
conditions <- list(
  x < 0,
  x < 1,
  is.na(x)
)
values <- list(
  "<0",
  "<1",
  NA
)
vec_case_when(
  conditions,
  values,
  default = "other"
)

# Both `values` and `default` are vectorized
values <- list(
  x * 5,
  x * 10,
  NA
)
vec_case_when(
  conditions,
  values,
  default = x * 100
)

# Use `vec_replace_when()` if you need to update `x`, retaining
# all previous values in locations that you don't match
conditions <- list(
  x < 0,
  x < 1
)
values <- list(
  0,
  1
)
out <- vec_replace_when(
  x,
  conditions,
  values
)
out

# Note how `vec_replace_when()` is type stable on `x`, we retain the
# integer type here even though `values` contained doubles
typeof(out)

# `vec_case_when()` creates a new vector, so names come from `values`
# and `default`. `vec_replace_when()` modifies an existing vector, so
# names come from `x` no matter what, just like `[<-` and `base::replace()`
x <- c(a = 1, b = 2, c = 3)
conditions <- list(x == 1, x == 2)
values <- list(c(x = 0), c(y = -1))
vec_case_when(conditions, values)
vec_replace_when(x, conditions, values)

# If you want to enforce that you've covered all of the locations in your
# `conditions`, use `unmatched = "error"` rather than providing a `default`
x <- c(0, 1, 2)
conditions <- list(x == 1, x == 2)
values <- list("a", "b")
try(vec_case_when(conditions, values, unmatched = "error"))