# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: row.match.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 6

suppressPackageStartupMessages(library(prodlim))
tab <- data.frame(num=1:26,abc=letters)
x <- c(3,"c")
row.match(x,tab)
x <- data.frame(n=c(3,8),z=c("c","h"))
row.match(x,tab)