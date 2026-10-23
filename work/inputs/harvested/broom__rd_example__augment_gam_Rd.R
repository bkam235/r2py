# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.gam.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 15

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("mgcv")) withAutoprint({ # examplesIf

# load libraries for models and data
library(mgcv)

# fit model
g <- gam(mpg ~ s(hp) + am + qsec, data = mtcars)

# summarize model fit with tidiers
tidy(g)
tidy(g, parametric = TRUE)
glance(g)
augment(g)
}) # examplesIf