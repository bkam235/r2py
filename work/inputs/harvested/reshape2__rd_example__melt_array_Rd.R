# r2py crawler metadata
# package: reshape2
# source_type: rd_example
# topic: melt.array.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\reshape2\help
# lines: 10

suppressPackageStartupMessages(library(reshape2))
a <- array(c(1:23, NA), c(2,3,4))
melt(a)
melt(a, na.rm = TRUE)
melt(a, varnames=c("X","Y","Z"))
dimnames(a) <- lapply(dim(a), function(x) LETTERS[1:x])
melt(a)
melt(a, varnames=c("X","Y","Z"))
dimnames(a)[1] <- list(NULL)
melt(a)