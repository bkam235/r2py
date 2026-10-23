# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: str2lang.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 6

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
str2lang <- getFromNamespace("str2lang", "backports")

str2lang("x[3] <- 1+4")