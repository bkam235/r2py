# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s36
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 10

suppressPackageStartupMessages(library(bit))
set.seed(1)
n <- 9L
x <- sample(n, replace=TRUE)
y <- sample(n, replace=TRUE)
x
y
x %in% y
bit_in(x, y)
bit_in(x, y, retFUN=as.logical)