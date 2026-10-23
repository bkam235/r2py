# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.negbin.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 13

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("MASS")) withAutoprint({ # examplesIf

# load libraries for models and data
library(MASS)

# fit model
r <- glm.nb(Days ~ Sex / (Age + Eth * Lrn), data = quine)

# summarize model fit with tidiers
tidy(r)
glance(r)
}) # examplesIf