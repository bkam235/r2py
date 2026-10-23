# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_unknown.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 19

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(Sacramento, package = "modeldata")

rec <-
  recipe(~ city + zip, data = Sacramento) |>
  step_unknown(city, new_level = "unknown city") |>
  step_unknown(zip, new_level = "unknown zip") |>
  prep()

table(bake(rec, new_data = NULL) |> pull(city),
  Sacramento |> pull(city),
  useNA = "always"
) |>
  as.data.frame() |>
  dplyr::filter(Freq > 0)

tidy(rec, number = 1)
}) # examplesIf