# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.regsubsets.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 12

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("leaps")) withAutoprint({ # examplesIf

# load libraries for models and data
library(leaps)

# fit model
all_fits <- regsubsets(hp ~ ., mtcars)

# summarize model fit with tidiers
tidy(all_fits)
}) # examplesIf