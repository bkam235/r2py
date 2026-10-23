# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: countpattern.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 4

suppressPackageStartupMessages(library(e1071))
xx <- rbind(c(1,0,0),c(1,0,0),c(1,0,1),c(0,1,1),c(0,1,1))
countpattern(xx)
countpattern(xx, matching=TRUE)