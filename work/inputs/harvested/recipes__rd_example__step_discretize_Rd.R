# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_discretize.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 19

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(biomass, package = "modeldata")

biomass_tr <- biomass[biomass$dataset == "Training", ]
biomass_te <- biomass[biomass$dataset == "Testing", ]

rec <- recipe(
  HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur,
  data = biomass_tr
) |>
  step_discretize(carbon, hydrogen)

rec <- prep(rec, biomass_tr)
binned_te <- bake(rec, biomass_te)
table(binned_te$carbon)

tidy(rec, 1)
}) # examplesIf