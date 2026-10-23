# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.muhaz.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 14

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("muhaz", "survival"))) withAutoprint({ # examplesIf

# load libraries for models and data
library(muhaz)
library(survival)

# fit model
x <- muhaz(ovarian$futime, ovarian$fustat)

# summarize model fit with tidiers
tidy(x)
glance(x)
}) # examplesIf