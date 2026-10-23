# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy_gam_hastie.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 13

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("gam")) withAutoprint({ # examplesIf

# load libraries for models and data
library(gam)

# fit model
g <- gam(mpg ~ s(hp, 4) + am + qsec, data = mtcars)

# summarize model fit with tidiers
tidy(g)
glance(g)
}) # examplesIf