# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_naomit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 5

suppressPackageStartupMessages(library(recipes))
recipe(Ozone ~ ., data = airquality) |>
  step_naomit(Solar.R) |>
  prep(airquality, verbose = FALSE) |>
  bake(new_data = NULL)