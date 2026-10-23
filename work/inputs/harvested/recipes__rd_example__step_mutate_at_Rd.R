# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_mutate_at.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 14

suppressPackageStartupMessages(library(recipes))
library(dplyr)
recipe(~., data = iris) |>
  step_mutate_at(contains("Length"), fn = ~ 1 / .) |>
  prep() |>
  bake(new_data = NULL) |>
  slice(1:10)

recipe(~., data = iris) |>
  # leads to more columns being created.
  step_mutate_at(contains("Length"), fn = list(log = log, sqrt = sqrt)) |>
  prep() |>
  bake(new_data = NULL) |>
  slice(1:10)