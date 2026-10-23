# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: reframe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 46

suppressPackageStartupMessages(library(dplyr))
table <- c("a", "b", "d", "f")

df <- tibble(
  g = c(1, 1, 1, 2, 2, 2, 2),
  x = c("e", "a", "b", "c", "f", "d", "a")
)

# `reframe()` allows you to apply functions that return
# an arbitrary number of rows
df |>
  reframe(x = intersect(x, table))

# Functions are applied per group, and each group can return a
# different number of rows.
df |>
  reframe(x = intersect(x, table), .by = g)

# The output is always ungrouped, even when using `group_by()`
df |>
  group_by(g) |>
  reframe(x = intersect(x, table))

# You can add multiple columns at once using a single expression by returning
# a data frame.
quantile_df <- function(x, probs = c(0.25, 0.5, 0.75)) {
  tibble(
    val = quantile(x, probs, na.rm = TRUE),
    quant = probs
  )
}

x <- c(10, 15, 18, 12)
quantile_df(x)

starwars |>
  reframe(quantile_df(height))

starwars |>
  reframe(quantile_df(height), .by = homeworld)

starwars |>
  reframe(
    across(c(height, mass), quantile_df, .unpack = TRUE),
    .by = homeworld
  )