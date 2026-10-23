# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: fully_trained.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 10

suppressPackageStartupMessages(library(recipes))
rec <- recipe(Species ~ ., data = iris) |>
  step_center(all_numeric())

rec |> fully_trained()


rec |>
  prep(training = iris) |>
  fully_trained()