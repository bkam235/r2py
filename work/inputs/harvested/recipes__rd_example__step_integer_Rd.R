# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_integer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 19

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(Sacramento, package = "modeldata")

sacr_tr <- Sacramento[1:100, ]
sacr_tr$sqft[1] <- NA

sacr_te <- Sacramento[101:105, ]
sacr_te$sqft[1] <- NA
sacr_te$city[1] <- "whoville"
sacr_te$city[2] <- NA

rec <- recipe(type ~ ., data = sacr_tr) |>
  step_integer(all_predictors()) |>
  prep(training = sacr_tr)

bake(rec, sacr_te, all_predictors())
tidy(rec, number = 1)
}) # examplesIf