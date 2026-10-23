# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
gf <- tibble(g = c(1, 1, 2, 2), x = c(0.5, 1.5, 2.5, 3.5))
gf |>
  group_by(g) |>
  mutate(x_mean = mean(x), x_rank = rank(x))