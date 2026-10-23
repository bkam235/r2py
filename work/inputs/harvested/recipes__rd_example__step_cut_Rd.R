# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_cut.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 38

suppressPackageStartupMessages(library(recipes))
df <- data.frame(x = 1:10, y = 5:14)
rec <- recipe(df)

# The min and max of the variable are used as boundaries
# if they exceed the breaks
rec |>
  step_cut(x, breaks = 5) |>
  prep() |>
  bake(df)

# You can use the same breaks on multiple variables
# then for each variable the boundaries are set separately
rec |>
  step_cut(x, y, breaks = c(6, 9)) |>
  prep() |>
  bake(df)

# You can keep the original variables using `step_mutate` or
# `step_mutate_at`, for transforming multiple variables at once
rec |>
  step_mutate(x_orig = x) |>
  step_cut(x, breaks = 5) |>
  prep() |>
  bake(df)

# It is up to you if you want values outside the
# range learned at prep to be included
new_df <- data.frame(x = 1:11, y = 5:15)
rec |>
  step_cut(x, breaks = 5, include_outside_range = TRUE) |>
  prep() |>
  bake(new_df)

rec |>
  step_cut(x, breaks = 5, include_outside_range = FALSE) |>
  prep() |>
  bake(new_df)