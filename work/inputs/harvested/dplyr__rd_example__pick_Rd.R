# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: pick.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 31

suppressPackageStartupMessages(library(dplyr))
df <- tibble(
  x = c(3, 2, 2, 2, 1),
  y = c(0, 2, 1, 1, 4),
  z1 = c("a", "a", "a", "b", "a"),
  z2 = c("c", "d", "d", "a", "c")
)
df

# `pick()` provides a way to select a subset of your columns using
# tidyselect. It returns a data frame.
df |> mutate(cols = pick(x, y))

# This is useful for functions that take data frames as inputs.
# For example, you can compute a joint rank between `x` and `y`.
df |> mutate(rank = dense_rank(pick(x, y)))

# `pick()` is also useful as a bridge between data-masking functions (like
# `mutate()` or `group_by()`) and functions with tidy-select behavior (like
# `select()`). For example, you can use `pick()` to create a wrapper around
# `group_by()` that takes a tidy-selection of columns to group on. For more
# bridge patterns, see
# https://rlang.r-lib.org/reference/topic-data-mask-programming.html#bridge-patterns.
my_group_by <- function(data, cols) {
  group_by(data, pick({{ cols }}))
}

df |> my_group_by(c(x, starts_with("z")))

# Or you can use it to dynamically select columns to `count()` by
df |> count(pick(starts_with("z")))