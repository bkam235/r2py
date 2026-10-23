# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_sample.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 23

suppressPackageStartupMessages(library(recipes))
# Uses `sample_n`
recipe(~., data = mtcars) |>
  step_sample(size = 1) |>
  prep(training = mtcars) |>
  bake(new_data = NULL) |>
  nrow()

# Uses `sample_frac`
recipe(~., data = mtcars) |>
  step_sample(size = 0.9999) |>
  prep(training = mtcars) |>
  bake(new_data = NULL) |>
  nrow()

# Uses `sample_n` and returns _at maximum_ 20 samples.
smaller_cars <-
  recipe(~., data = mtcars) |>
  step_sample() |>
  prep(training = mtcars |> slice(1:20))

bake(smaller_cars, new_data = NULL) |> nrow()
bake(smaller_cars, new_data = mtcars |> slice(21:32)) |> nrow()