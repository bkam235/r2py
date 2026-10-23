# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.binWidth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 14

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("binGroup")) withAutoprint({ # examplesIf

# load libraries
library(binGroup)

# fit model
bw <- binWidth(100, .1)

bw

# summarize model fit with tidiers
tidy(bw)
}) # examplesIf