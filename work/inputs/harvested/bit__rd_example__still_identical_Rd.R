# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: still.identical.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 6

suppressPackageStartupMessages(library(bit))
x <- 1:2
y <- x
z <- copy_vector(x)
still.identical(y, x)
still.identical(z, x)