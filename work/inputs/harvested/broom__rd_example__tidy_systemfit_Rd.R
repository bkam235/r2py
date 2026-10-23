# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.systemfit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 23

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("systemfit")) withAutoprint({ # examplesIf

set.seed(27)

# load libraries for models and data
library(systemfit)

# generate data
df <- data.frame(
  X = rnorm(100),
  Y = rnorm(100),
  Z = rnorm(100),
  W = rnorm(100)
)

# fit model
fit <- systemfit(formula = list(Y ~ Z, W ~ X), data = df, method = "SUR")

# summarize model fit with tidiers
tidy(fit)
tidy(fit, conf.int = TRUE)
}) # examplesIf