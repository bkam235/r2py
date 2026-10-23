# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: check_cols.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 12

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(biomass, package = "modeldata")

biomass_rec <- recipe(HHV ~ ., data = biomass) |>
  step_rm(sample, dataset) |>
  check_cols(contains("gen")) |>
  step_center(all_numeric_predictors())

bake(biomass_rec, biomass[, c("carbon", "HHV")])

}) # examplesIf