# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: hamming.distance.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 9

suppressPackageStartupMessages(library(e1071))
x <- c(1, 0, 0)
y <- c(1, 0, 1)
hamming.distance(x, y)
z <- rbind(x,y)
rownames(z) <- c("Fred", "Tom")
hamming.distance(z)

hamming.distance(1:3, 3:1)