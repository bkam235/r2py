# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: has_element.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 4

suppressPackageStartupMessages(library(purrr))
x <- list(1:10, 5, 9.9)
x |> has_element(1:10)
x |> has_element(3)