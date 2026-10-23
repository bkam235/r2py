# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: file.size.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 11

suppressPackageStartupMessages(library(backports))
# get functions from namespace instead of possibly getting
# implementations shipped with recent R versions:
bp_file.size = getFromNamespace("file.size", "backports")
bp_file.mode = getFromNamespace("file.size", "backports")
bp_file.mtime = getFromNamespace("file.size", "backports")

fn = file.path(R.home(), "COPYING")
bp_file.size(fn)
bp_file.mode(fn)
bp_file.size(fn)