# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_nnmf.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 16

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed(c("modeldata", "ggplot2"))) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(biomass, package = "modeldata")

# rec <- recipe(HHV ~ ., data = biomass) |>
#   update_role(sample, new_role = "id var") |>
#   update_role(dataset, new_role = "split variable") |>
#   step_nnmf(all_numeric_predictors(), num_comp = 2, seed = 473, num_run = 2) |>
#   prep(training = biomass)
#
# bake(rec, new_data = NULL)
#
# library(ggplot2)
# bake(rec, new_data = NULL) |>
#  ggplot(aes(x = NNMF2, y = NNMF1, col = HHV)) + geom_point()
}) # examplesIf