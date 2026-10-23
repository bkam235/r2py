# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.survdiff.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 16

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("survival")) withAutoprint({ # examplesIf

# load libraries for models and data
library(survival)

# fit model
s <- survdiff(
  Surv(time, status) ~ pat.karno + strata(inst),
  data = lung
)

# summarize model fit with tidiers
tidy(s)
glance(s)
}) # examplesIf