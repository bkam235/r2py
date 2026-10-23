# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: paste.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 5

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_paste = getFromNamespace("paste", "backports")
bp_paste(letters[1:3], character(), collapse = NULL, recycle0 = TRUE)