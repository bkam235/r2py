# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: list2DF.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 6

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_list2DF = getFromNamespace("list2DF", "backports")

bp_list2DF(list(x = 1:3, y = 2:4))