# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: firstNA.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 8

suppressPackageStartupMessages(library(bit))
x <- c(FALSE, NA, TRUE)
firstNA(x)
reverse_vector(x)

x <- 1:1e7
system.time(rev(x))
system.time(reverse_vector(x))