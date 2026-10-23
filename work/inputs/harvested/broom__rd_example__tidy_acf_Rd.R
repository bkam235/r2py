# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.acf.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 4

suppressPackageStartupMessages(library(broom))
tidy(acf(lh, plot = FALSE))
tidy(ccf(mdeaths, fdeaths, plot = FALSE))
tidy(pacf(lh, plot = FALSE))