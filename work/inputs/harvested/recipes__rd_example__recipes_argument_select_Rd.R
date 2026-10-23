# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: recipes_argument_select.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 14

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
library(rlang)
data(scat, package = "modeldata")

rec <- recipe(Species ~ ., data = scat)

info <- summary(rec)
info

recipes_argument_select(quos(Year), scat, info)
recipes_argument_select(vars(Year), scat, info)
recipes_argument_select(imp_vars(Year), scat, info)
}) # examplesIf