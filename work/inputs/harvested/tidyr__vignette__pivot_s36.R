# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s36
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 9

suppressPackageStartupMessages(library(tidyr))
updates <- tibble(
  county = c("Wake", "Wake", "Wake", "Guilford", "Guilford"),
  date = c(as.Date("2020-01-01") + 0:2, as.Date("2020-01-03") + 0:1),
  system = c("A", "B", "C", "A", "C"),
  value = c(3.2, 4, 5.5, 2, 1.2)
)

updates