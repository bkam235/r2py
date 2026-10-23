# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.glmRob.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 13

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("robust")) withAutoprint({ # examplesIf

# load libraries for models and data
library(robust)

# fit model
gm <- glmRob(am ~ wt, data = mtcars, family = "binomial")

# summarize model fit with tidiers
tidy(gm)
glance(gm)
}) # examplesIf