# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: hasName.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 6

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_hasName = getFromNamespace("hasName", "backports")

bp_hasName(list(a = 1, b = 2), c("a", "b", "c"))