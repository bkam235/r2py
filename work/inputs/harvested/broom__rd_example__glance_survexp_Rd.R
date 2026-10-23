# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.survexp.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 22

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("survival")) withAutoprint({ # examplesIf

# load libraries for models and data
library(survival)

# fit model
sexpfit <- survexp(
  futime ~ 1,
  rmap = list(
    sex = "male",
    year = accept.dt,
    age = (accept.dt - birth.dt)
  ),
  method = "conditional",
  data = jasa
)

# summarize model fit with tidiers
tidy(sexpfit)
glance(sexpfit)
}) # examplesIf