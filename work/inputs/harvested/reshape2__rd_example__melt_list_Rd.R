# r2py crawler metadata
# package: reshape2
# source_type: rd_example
# topic: melt.list.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\reshape2\help
# lines: 11

suppressPackageStartupMessages(library(reshape2))
a <- as.list(c(1:4, NA))
melt(a)
names(a) <- letters[1:4]
melt(a)
a <- list(matrix(1:4, ncol=2), matrix(1:6, ncol=2))
melt(a)
a <- list(matrix(1:4, ncol=2), array(1:27, c(3,3,3)))
melt(a)
melt(list(1:5, matrix(1:4, ncol=2)))
melt(list(list(1:3), 1, list(as.list(3:4), as.list(1:2))))