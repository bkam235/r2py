# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: tidy.recipe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 21

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(Sacramento, package = "modeldata")

Sacramento_rec <- recipe(~., data = Sacramento) |>
  step_other(all_nominal(), threshold = 0.05, other = "another") |>
  step_center(all_numeric()) |>
  step_dummy(all_nominal()) |>
  check_cols(ends_with("ude"), sqft, price)

tidy(Sacramento_rec)

tidy(Sacramento_rec, number = 2)
tidy(Sacramento_rec, number = 3)

Sacramento_rec_trained <- prep(Sacramento_rec, training = Sacramento)

tidy(Sacramento_rec_trained)
tidy(Sacramento_rec_trained, number = 3)
tidy(Sacramento_rec_trained, number = 4)
}) # examplesIf