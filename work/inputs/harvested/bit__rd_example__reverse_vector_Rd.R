# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: reverse_vector.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 8

suppressPackageStartupMessages(library(bit))
x <- factor(letters)
rev(x)
reverse_vector(x)

x <- 1:1e7
system.time(rev(x))
system.time(reverse_vector(x))