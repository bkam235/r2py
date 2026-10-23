# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.lmRob.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 14

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("robust")) withAutoprint({ # examplesIf

# load modeling library
library(robust)

# fit model
m <- lmRob(mpg ~ wt, data = mtcars)

# summarize model fit with tidiers
tidy(m)
augment(m)
glance(m)
}) # examplesIf