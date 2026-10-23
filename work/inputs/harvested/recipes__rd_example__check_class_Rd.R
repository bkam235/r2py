# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: check_class.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 38

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
library(dplyr)
data(Sacramento, package = "modeldata")

# Learn the classes on the train set
train <- Sacramento[1:500, ]
test <- Sacramento[501:nrow(Sacramento), ]
recipe(train, sqft ~ .) |>
  check_class(everything()) |>
  prep(train, strings_as_factors = FALSE) |>
  bake(test)

# Manual specification
recipe(train, sqft ~ .) |>
  check_class(sqft, class_nm = "integer") |>
  check_class(city, zip, type, class_nm = "factor") |>
  check_class(latitude, longitude, class_nm = "numeric") |>
  prep(train, strings_as_factors = FALSE) |>
  bake(test)

# By default only the classes that are specified
#   are allowed.
x_df <- tibble(time = c(Sys.time() - 60, Sys.time()))
x_df$time |> class()

recipe(x_df) |>
  check_class(time, class_nm = "POSIXt") |>
  prep(x_df) |>
  bake_(x_df)


# Use allow_additional = TRUE if you are fine with it
recipe(x_df) |>
  check_class(time, class_nm = "POSIXt", allow_additional = TRUE) |>
  prep(x_df) |>
  bake(x_df)
}) # examplesIf