# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: read.matrix.csr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 12

suppressPackageStartupMessages(library(e1071))
library(methods)
if (require(SparseM)) {
    data(iris)
    x <- as.matrix(iris[,1:4])
    y <- iris[,5]
    xs <- as.matrix.csr(x)
    write.matrix.csr(xs, y = y, file = "iris.dat")
    xs2 <- read.matrix.csr("iris.dat")$x
    if (!all(as.matrix(xs) == as.matrix(xs2)))
        stop("Error: objects are not equal!")
}