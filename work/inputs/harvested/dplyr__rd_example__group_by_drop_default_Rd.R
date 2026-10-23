# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: group_by_drop_default.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 10

suppressPackageStartupMessages(library(dplyr))
group_by_drop_default(iris)

iris |>
  group_by(Species) |>
  group_by_drop_default()

iris |>
  group_by(Species, .drop = FALSE) |>
  group_by_drop_default()