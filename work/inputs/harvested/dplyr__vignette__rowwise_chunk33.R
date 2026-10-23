# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_chunk33
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.Rmd
# lines: 4

suppressPackageStartupMessages(library(dplyr))
mtcars |>
      group_by(cyl) |>
      do(head(., 1))