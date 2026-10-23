# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: when-any-all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 91

suppressPackageStartupMessages(library(dplyr))
x <- c(TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, NA, NA, NA)
y <- c(TRUE, FALSE, NA, TRUE, FALSE, NA, TRUE, FALSE, NA)

# `any()` and `all()` summarise down to 1 value
any(x, y)
all(x, y)

# `when_any()` and `when_all()` work element by element across all inputs
# at the same time. Their defaults are equivalent to calling `|` or `&`.
when_any(x, y)
x | y

when_all(x, y)
x & y

# `na_rm = TRUE` is useful when you'd like to force these functions to
# return only `TRUE` or `FALSE`. This argument does so by removing any `NA`
# from the elementwise computation entirely.
tibble(
  x = x,
  y = y,
  any_propagate = when_any(x, y),
  any_remove = when_any(x, y, na_rm = TRUE),
  all_propagate = when_all(x, y),
  all_remove = when_all(x, y, na_rm = TRUE)
)

# ---------------------------------------------------------------------------
# With `filter()` and `filter_out()`

# `when_any()` is particularly useful inside of `filter()` and
# `filter_out()` as a way to combine comma separated conditions with `|`
# instead of with `&`.

countries <- tibble(
  name = c("US", "CA", "PR", "RU", "US", NA, "CA", "PR", "RU"),
  score = c(200, 100, 150, NA, 50, 100, 300, 250, 120)
)
countries

# Find rows where any of the following are true:
# - "US" and "CA" have a score between 200-300
# - "PR" and "RU" have a score between 100-200
countries |>
  filter(
    (name %in% c("US", "CA") & between(score, 200, 300)) |
      (name %in% c("PR", "RU") & between(score, 100, 200))
  )

# With `when_any()`, you drop the explicit `|`, the extra `()`, and your
# conditions are all indented to the same level
countries |>
  filter(when_any(
    name %in% c("US", "CA") & between(score, 200, 300),
    name %in% c("PR", "RU") & between(score, 100, 200)
  ))

# To drop these rows instead, use `filter_out()`
countries |>
  filter_out(when_any(
    name %in% c("US", "CA") & between(score, 200, 300),
    name %in% c("PR", "RU") & between(score, 100, 200)
  ))

# ---------------------------------------------------------------------------
# Programming with `when_any()` and `when_all()`

# The `size` argument is useful for making these functions size stable when
# you aren't sure how many inputs you're going to receive
size <- length(x)

# Two inputs
inputs <- list(x, y)
when_all(!!!inputs, size = size)

# One input
inputs <- list(x)
when_all(!!!inputs, size = size)

# Zero inputs (without `size`, this would return `logical()`)
inputs <- list()
when_all(!!!inputs, size = size)

# When no inputs are provided, these functions are consistent with `any()`
# and `all()`
any()
when_any(size = 1)

all()
when_all(size = 1)