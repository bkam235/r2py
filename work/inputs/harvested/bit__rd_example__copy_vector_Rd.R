# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: copy_vector.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 9

suppressPackageStartupMessages(library(bit))
x <- factor(letters)
y <- x
z <- copy_vector(x)
still.identical(x, y)
still.identical(x, z)
str(x)
str(y)
str(z)