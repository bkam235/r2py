# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: op_concat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 8

suppressPackageStartupMessages(library(lava))
## Block diagonal
matrix(rnorm(25),5)%++%matrix(rnorm(25),5)
## String concatenation
"Hello "%++%" World"
## Function composition
f <- log %++% exp
f(2)