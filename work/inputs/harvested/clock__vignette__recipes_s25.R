# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s25
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 8

suppressPackageStartupMessages(library(clock))
try({
date_seq(
  date_build(2019, 1, 1),
  to = date_build(2019, 10, 2),
  by = duration_months(2)
)
})