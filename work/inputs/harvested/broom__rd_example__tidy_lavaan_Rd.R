# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.lavaan.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 12

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("lavaan")) withAutoprint({ # examplesIf

# load libraries for models and data
library(lavaan)

cfa.fit <- cfa("F =~ x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9",
  data = HolzingerSwineford1939, group = "school"
)

tidy(cfa.fit)
}) # examplesIf