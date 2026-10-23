# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.aareg.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 16

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("survival")) withAutoprint({ # examplesIf

# load libraries for models and data
library(survival)

# fit model
afit <- aareg(
  Surv(time, status) ~ age + sex + ph.ecog,
  data = lung,
  dfbeta = TRUE
)

# summarize model fit with tidiers
tidy(afit)
}) # examplesIf