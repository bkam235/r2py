# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: paste0.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 5

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_paste0 = getFromNamespace("paste0", "backports")
bp_paste0(letters[1:3], character(), collapse = NULL, recycle0 = TRUE)