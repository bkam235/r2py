# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: group_trim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 5

suppressPackageStartupMessages(library(dplyr))
iris |>
  group_by(Species) |>
  filter(Species == "setosa", .preserve = TRUE) |>
  group_trim()