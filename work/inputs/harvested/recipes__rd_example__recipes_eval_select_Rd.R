# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: recipes_eval_select.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 14

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
library(rlang)
data(scat, package = "modeldata")

rec <- recipe(Species ~ ., data = scat)

info <- summary(rec)
info

quos <- quos(all_numeric_predictors(), where(is.factor))

recipes_eval_select(quos, scat, info)
}) # examplesIf