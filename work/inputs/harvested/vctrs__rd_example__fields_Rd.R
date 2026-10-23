# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: fields.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 8

suppressPackageStartupMessages(library(vctrs))
x <- new_rcrd(list(x = 1:3, y = 3:1, z = letters[1:3]))
n_fields(x)
fields(x)

field(x, "y")
field(x, "y") <- runif(3)
field(x, "y")