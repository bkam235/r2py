# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: detect_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 5

suppressPackageStartupMessages(library(recipes))
rec <- recipe(Species ~ ., data = iris) |>
  step_intercept()

detect_step(rec, "intercept")