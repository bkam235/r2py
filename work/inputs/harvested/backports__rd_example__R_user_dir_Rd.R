# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: R_user_dir.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 6

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_R_user_dir = getFromNamespace("R_user_dir", "backports")

bp_R_user_dir("backports")