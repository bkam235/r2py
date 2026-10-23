# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_dummy.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 47

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(Sacramento, package = "modeldata")

# Original data: city has 37 levels
length(unique(Sacramento$city))
unique(Sacramento$city) |> sort()

rec <- recipe(~ city + sqft + price, data = Sacramento)

# Default dummy coding: 36 dummy variables
dummies <- rec |>
  step_dummy(city) |>
  prep()

dummy_data <- bake(dummies, new_data = NULL)

dummy_data |>
  select(starts_with("city")) |>
  glimpse() # level "anything" is the reference level

# Obtain the full set of 37 dummy variables using `one_hot` option
dummies_one_hot <- rec |>
  step_dummy(city, one_hot = TRUE) |>
  prep()

dummy_data_one_hot <- bake(dummies_one_hot, new_data = NULL)

dummy_data_one_hot |>
  select(starts_with("city")) |>
  glimpse() # no reference level

# Obtain the full set of 37 dummy variables using helmert contrasts
dummies_helmert <- rec |>
  step_dummy(city, contrasts = "contr.helmert") |>
  prep()

dummy_data_helmert <- bake(dummies_helmert, new_data = NULL)

dummy_data_helmert |>
  select(starts_with("city")) |>
  glimpse() # no reference level

tidy(dummies, number = 1)
tidy(dummies_one_hot, number = 1)
tidy(dummies_helmert, number = 1)
}) # examplesIf