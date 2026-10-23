# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: fctr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 6

suppressPackageStartupMessages(library(data.table))
levels(factor(c("b","a","c")))
levels(fctr(c("b","a","c")))
levels(fctr(c("b","a","c"), rev=TRUE))
levels(fctr(c("b","a","c"), sort=TRUE))
levels(fctr(c("b","a","c"), sort=TRUE, rev=TRUE))