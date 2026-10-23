# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: trimws.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 7

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_trimws = getFromNamespace("trimws", "backports")
bp_trimws(c("  a  ", "b  ", "  c"))

bp_trimws(c("  a  ", "b  ", "  c"), which = "left")