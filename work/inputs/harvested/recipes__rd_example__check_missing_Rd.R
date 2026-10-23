# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: check_missing.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 32

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(credit_data, package = "modeldata")
is.na(credit_data) |> colSums()

# If the test passes, `new_data` is returned unaltered
recipe(credit_data) |>
  check_missing(Age, Expenses) |>
  prep() |>
  bake(credit_data)

# If your training set doesn't pass, prep() will stop with an error

recipe(credit_data) |>
  check_missing(Income) |>
  prep()


# If `new_data` contain missing values, the check will stop `bake()`

train_data <- credit_data |> dplyr::filter(Income > 150)
test_data <- credit_data |> dplyr::filter(Income <= 150 | is.na(Income))

rp <- recipe(train_data) |>
  check_missing(Income) |>
  prep()

bake(rp, train_data)

bake(rp, test_data)

}) # examplesIf