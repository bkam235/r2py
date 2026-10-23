# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.R
# lines: 10

suppressPackageStartupMessages(library(dplyr))
df <- tibble(name = c("Mara", "Hadley"), x = 1:2, y = 3:4, z = 5:6)

df |>
  rowwise() |>
  summarise(m = mean(c(x, y, z)))

df |>
  rowwise(name) |>
  summarise(m = mean(c(x, y, z)))