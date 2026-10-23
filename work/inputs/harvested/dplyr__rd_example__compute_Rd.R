# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: compute.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 18

suppressPackageStartupMessages(library(dplyr))
if (requireNamespace("dbplyr", quietly = TRUE) && requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
mtcars2 <- dbplyr::src_memdb() |>
  copy_to(mtcars, name = "mtcars2-cc", overwrite = TRUE)

remote <- mtcars2 |>
  filter(cyl == 8) |>
  select(mpg:drat)

# Compute query and save in remote table
compute(remote)

# Compute query bring back to this session
collect(remote)

# Creates a fresh query based on the generated SQL
collapse(remote)
}) # examplesIf