# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: get0.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 10

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_get0 = getFromNamespace("get0", "backports")

bp_get0("a")
bp_get0("a", ifnotfound = 0)

foo = 12
bp_get0("foo")