# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: c_across.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 8

suppressPackageStartupMessages(library(dplyr))
df <- tibble(id = 1:4, w = runif(4), x = runif(4), y = runif(4), z = runif(4))
df |>
  rowwise() |>
  mutate(
    sum = sum(c_across(w:z)),
    sd = sd(c_across(w:z))
  )