# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: unnest_longer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 35

suppressPackageStartupMessages(library(tidyr))
# `unnest_longer()` is useful when each component of the list should
# form a row
df <- tibble(
  x = 1:4,
  y = list(NULL, 1:3, 4:5, integer())
)
df |> unnest_longer(y)

# Note that empty values like `NULL` and `integer()` are dropped by
# default. If you'd like to keep them, set `keep_empty = TRUE`.
df |> unnest_longer(y, keep_empty = TRUE)

# If the inner vectors are named, the names are copied to an `_id` column
df <- tibble(
  x = 1:2,
  y = list(c(a = 1, b = 2), c(a = 10, b = 11, c = 12))
)
df |> unnest_longer(y)

# Multiple columns ----------------------------------------------------------
# If columns are aligned, you can unnest simultaneously
df <- tibble(
  x = 1:2,
  y = list(1:2, 3:4),
  z = list(5:6, 7:8)
)
df |>
  unnest_longer(c(y, z))

# This is important because sequential unnesting would generate the
# Cartesian product of the rows
df |>
  unnest_longer(y) |>
  unnest_longer(z)