# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: list-of-attributes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 8

suppressPackageStartupMessages(library(vctrs))
x <- list_of(1, 2)
list_of_ptype(x)
list_of_size(x)

x <- list_of(.ptype = integer(), .size = 5)
list_of_ptype(x)
list_of_size(x)