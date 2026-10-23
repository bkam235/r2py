# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: dotsNames.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 7

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_...names = getFromNamespace("...names", "backports")

foo = function(...) bp_...names()
foo(a = 1, b = 2, 3)