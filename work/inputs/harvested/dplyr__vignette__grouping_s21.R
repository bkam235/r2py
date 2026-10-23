# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: grouping_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\grouping.R
# lines: 11

suppressPackageStartupMessages(library(dplyr))
# Overall rank
starwars |>
  select(name, homeworld, height) |>
  mutate(rank = min_rank(height))

# Rank per homeworld
starwars |>
  select(name, homeworld, height) |>
  group_by(homeworld) |>
  mutate(rank = min_rank(height))