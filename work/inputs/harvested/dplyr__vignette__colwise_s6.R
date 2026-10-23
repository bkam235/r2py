# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
df <- data.frame(g = c(1, 1, 2), x = c(-1, 1, 3), y = c(-1, -4, -9))
df |>
  group_by(g) |>
  summarise(across(where(is.numeric), sum))