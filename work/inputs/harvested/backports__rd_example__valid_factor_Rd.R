# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: valid.factor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 5

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_.valid_factor = getFromNamespace(".valid.factor", "backports")
bp_.valid_factor(factor(letters[1:3]))