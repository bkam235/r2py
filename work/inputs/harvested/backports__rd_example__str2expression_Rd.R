# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: str2expression.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 6

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
str2expression <- getFromNamespace("str2expression", "backports")

str2expression("x[3] <- 1+4")