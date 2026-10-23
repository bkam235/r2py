# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: dir.exists.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 6

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_dir.exists = getFromNamespace("dir.exists", "backports")

bp_dir.exists(tempdir())