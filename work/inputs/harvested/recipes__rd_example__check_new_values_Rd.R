# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: check_new_values.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 34

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(credit_data, package = "modeldata")

# If the test passes, `new_data` is returned unaltered
recipe(credit_data) |>
  check_new_values(Home) |>
  prep() |>
  bake(new_data = credit_data)

# If `new_data` contains values not in `x` at the [prep()] function,
# the [bake()] function will break.

recipe(credit_data |> dplyr::filter(Home != "rent")) |>
  check_new_values(Home) |>
  prep() |>
  bake(new_data = credit_data)


# By default missing values are ignored, so this passes.
recipe(credit_data |> dplyr::filter(!is.na(Home))) |>
  check_new_values(Home) |>
  prep() |>
  bake(credit_data)

# Use `ignore_NA = FALSE` if you consider missing values  as a value,
# that should not occur when not observed in the train set.

recipe(credit_data |> dplyr::filter(!is.na(Home))) |>
  check_new_values(Home, ignore_NA = FALSE) |>
  prep() |>
  bake(credit_data)

}) # examplesIf