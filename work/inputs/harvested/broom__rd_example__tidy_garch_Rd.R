# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.garch.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 18

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("tseries")) withAutoprint({ # examplesIf

# load libraries for models and data
library(tseries)

# load data
data(EuStockMarkets)

# fit model
dax <- diff(log(EuStockMarkets))[, "DAX"]
dax.garch <- garch(dax)
dax.garch

# summarize model fit with tidiers
tidy(dax.garch)
glance(dax.garch)
}) # examplesIf