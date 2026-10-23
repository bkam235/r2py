# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.geeglm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 23

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("geepack")) withAutoprint({ # examplesIf

# load modeling library
library(geepack)

# load data
data(state)


ds <- data.frame(state.region, state.x77)

# fit model
geefit <- geeglm(Income ~ Frost + Murder,
  id = state.region,
  data = ds,
  corstr = "exchangeable"
)

# summarize model fit with tidiers
tidy(geefit)
tidy(geefit, conf.int = TRUE)
}) # examplesIf