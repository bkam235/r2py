# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_relevel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 11

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(Sacramento, package = "modeldata")
rec <- recipe(~ city + zip, data = Sacramento) |>
  step_unknown(city, new_level = "UNKNOWN") |>
  step_relevel(city, ref_level = "UNKNOWN") |>
  prep()

data <- bake(rec, Sacramento)
levels(data$city)
}) # examplesIf