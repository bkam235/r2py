# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.drc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 19

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("drc")) withAutoprint({ # examplesIf

# load libraries for models and data
library(drc)

# fit model
mod <- drm(dead / total ~ conc, type,
  weights = total, data = selenium, fct = LL.2(), type = "binomial"
)

# summarize model fit with tidiers
tidy(mod)
tidy(mod, conf.int = TRUE)

glance(mod)

augment(mod, selenium)
}) # examplesIf