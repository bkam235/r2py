# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: diffCsv.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 10

suppressPackageStartupMessages(library(diffobj))
iris.2 <- iris
iris.2$Sepal.Length[5] <- 99
f1 <- tempfile()
f2 <- tempfile()
write.csv(iris, f1, row.names=FALSE)
write.csv(iris.2, f2, row.names=FALSE)
## `pager="off"` for CRAN compliance; you may omit in normal use
diffCsv(f1, f2, pager="off")
unlink(c(f1, f2))