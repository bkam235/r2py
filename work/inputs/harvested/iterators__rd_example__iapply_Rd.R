# r2py crawler metadata
# package: iterators
# source_type: rd_example
# topic: iapply.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\iterators\help
# lines: 14

suppressPackageStartupMessages(library(iterators))
a <- array(1:8, c(2, 2, 2))

# iterate over all the matrices
it <- iapply(a, 3)
as.list(it)

# iterate over all the columns of all the matrices
it <- iapply(a, c(2, 3))
as.list(it)

# iterate over all the rows of all the matrices
it <- iapply(a, c(1, 3))
as.list(it)