# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: get_data_types.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 6

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf

data(Sacramento, package = "modeldata")
lapply(Sacramento, .get_data_types)
}) # examplesIf