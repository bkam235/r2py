# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: boxplot.bclust.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 4

suppressPackageStartupMessages(library(e1071))
data(iris)
bc1 <- bclust(iris[,1:4], 3, base.centers=5)
boxplot(bc1)