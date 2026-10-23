# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.lavaan.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 14

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("lavaan")) withAutoprint({ # examplesIf

library(lavaan)

# fit model
cfa.fit <- cfa(
  "F =~ x1 + x2 + x3 + x4 + x5",
  data = HolzingerSwineford1939, group = "school"
)

# summarize model fit with tidiers
glance(cfa.fit)
}) # examplesIf