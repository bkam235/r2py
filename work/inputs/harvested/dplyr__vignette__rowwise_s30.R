# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_s30
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.R
# lines: 6

suppressPackageStartupMessages(library(dplyr))
df <- expand.grid(mean = c(-1, 0, 1), sd = c(1, 10, 100))

df |>
  rowwise() |>
  mutate(data = list(rnorm(10, mean, sd)))