# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_pls.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 46

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# requires the Bioconductor mixOmics package
data(biomass, package = "modeldata")

biom_tr <-
  biomass |>
  dplyr::filter(dataset == "Training") |>
  dplyr::select(-dataset, -sample)
biom_te <-
  biomass |>
  dplyr::filter(dataset == "Testing") |>
  dplyr::select(-dataset, -sample, -HHV)

dense_pls <-
  recipe(HHV ~ ., data = biom_tr) |>
  step_pls(all_numeric_predictors(), outcome = HHV, num_comp = 3)

sparse_pls <-
  recipe(HHV ~ ., data = biom_tr) |>
  step_pls(all_numeric_predictors(), outcome = HHV, num_comp = 3,
           predictor_prop = 4 / 5)

## -----------------------------------------------------------------------------
## PLS discriminant analysis

data(cells, package = "modeldata")

cell_tr <-
  cells |>
  dplyr::filter(case == "Train") |>
  dplyr::select(-case)
cell_te <-
  cells |>
  dplyr::filter(case == "Test") |>
  dplyr::select(-case, -class)

dense_plsda <-
  recipe(class ~ ., data = cell_tr) |>
  step_pls(all_numeric_predictors(), outcome = class, num_comp = 5)

sparse_plsda <-
  recipe(class ~ ., data = cell_tr) |>
  step_pls(all_numeric_predictors(), outcome = class, num_comp = 5,
           predictor_prop = 1 / 4)
}) # examplesIf