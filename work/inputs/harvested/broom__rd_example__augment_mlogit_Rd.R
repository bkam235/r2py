# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.mlogit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 17

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("mlogit")) withAutoprint({ # examplesIf

# load libraries for models and data
library(mlogit)

data("Fishing", package = "mlogit")
Fish <- dfidx(Fishing, varying = 2:9, shape = "wide", choice = "mode")

# fit model
m <- mlogit(mode ~ price + catch | income, data = Fish)

# summarize model fit with tidiers
tidy(m)
augment(m)
glance(m)
}) # examplesIf