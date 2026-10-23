# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_factor2string.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 22

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(Sacramento, package = "modeldata")

rec <- recipe(~ city + zip, data = Sacramento)

make_string <- rec |>
  step_factor2string(city)

make_string <- prep(make_string,
  training = Sacramento,
  strings_as_factors = FALSE
)

make_string

# note that `city` is a string in recipe output
bake(make_string, new_data = NULL) |> head()

# ...but remains a factor in the original data
Sacramento |> head()
}) # examplesIf