# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_rename_at.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 7

suppressPackageStartupMessages(library(recipes))
library(dplyr)
recipe(~., data = iris) |>
  step_rename_at(all_predictors(), fn = ~ gsub(".", "_", ., fixed = TRUE)) |>
  prep() |>
  bake(new_data = NULL) |>
  slice(1:10)