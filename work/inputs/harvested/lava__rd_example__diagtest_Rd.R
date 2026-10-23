# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: diagtest.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 5

suppressPackageStartupMessages(library(lava))
M <- as.table(matrix(c(42,12,
                       35,28),ncol=2,byrow=TRUE,
                     dimnames=list(rater=c("no","yes"),gold=c("no","yes"))))
diagtest(M,exact=TRUE)