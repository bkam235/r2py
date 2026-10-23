# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: with_groups.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 8

suppressPackageStartupMessages(library(dplyr))
df <- tibble(g = c(1, 1, 2, 2, 3), x = runif(5))

# Old
df |>
  with_groups(g, mutate, x_mean = mean(x))
# New
df |> mutate(x_mean = mean(x), .by = g)