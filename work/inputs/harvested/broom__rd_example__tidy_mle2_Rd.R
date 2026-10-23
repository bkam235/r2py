# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.mle2.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 19

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("bbmle")) withAutoprint({ # examplesIf

# load libraries for models and data
library(bbmle)

# generate data
x <- 0:10
y <- c(26, 17, 13, 12, 20, 5, 9, 8, 5, 4, 8)
d <- data.frame(x, y)

# fit model
fit <- mle2(y ~ dpois(lambda = ymean),
  start = list(ymean = mean(y)), data = d
)

# summarize model fit with tidiers
tidy(fit)
}) # examplesIf