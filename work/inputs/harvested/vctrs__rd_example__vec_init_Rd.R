# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_init.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 9

suppressPackageStartupMessages(library(vctrs))
vec_init(1:10, 3)
vec_init(Sys.Date(), 5)

# The "missing" value for a data frame is a row that is entirely missing
vec_init(mtcars, 2)

# The "missing" value for a list is `NULL`
vec_init(list(), 3)