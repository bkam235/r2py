# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.varest.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 16

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("vars")) withAutoprint({ # examplesIf

# load libraries for models and data
library(vars)

# load data
data("Canada", package = "vars")

# fit models
mod <- VAR(Canada, p = 1, type = "both")

# summarize model fit with tidiers
tidy(mod)
glance(mod)
}) # examplesIf