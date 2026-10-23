# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: warningCondition.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 5

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_warningCondition = getFromNamespace("warningCondition", "backports")
bp_warningCondition("package backports not found")