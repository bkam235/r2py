# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_s29
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.R
# lines: 6

suppressPackageStartupMessages(library(dplyr))
try({
df |>
  rowwise() |>
  mutate(data = runif(n, min, max))
})