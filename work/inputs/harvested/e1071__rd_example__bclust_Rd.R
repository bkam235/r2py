# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: bclust.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 7

suppressPackageStartupMessages(library(e1071))
data(iris)
bc1 <- bclust(iris[,1:4], 3, base.centers=5)
plot(bc1)

table(clusters.bclust(bc1, 3))
centers.bclust(bc1, 3)