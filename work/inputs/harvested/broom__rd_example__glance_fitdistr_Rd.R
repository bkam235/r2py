# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.fitdistr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 17

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("MASS")) withAutoprint({ # examplesIf

# load libraries for models and data
library(MASS)

# generate data
set.seed(2015)
x <- rnorm(100, 5, 2)

#  fit models
fit <- fitdistr(x, dnorm, list(mean = 3, sd = 1))

# summarize model fit with tidiers
tidy(fit)
glance(fit)
}) # examplesIf