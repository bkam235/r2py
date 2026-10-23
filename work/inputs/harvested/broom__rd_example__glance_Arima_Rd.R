# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.Arima.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 7

suppressPackageStartupMessages(library(broom))
# fit model
fit <- arima(lh, order = c(1, 0, 0))

# summarize model fit with tidiers
tidy(fit)
glance(fit)