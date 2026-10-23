# r2py crawler metadata
# package: future
# source_type: rd_example
# topic: futureSessionInfo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future\help
# lines: 4

suppressPackageStartupMessages(library(future))
plan(multisession, workers = 2)
futureSessionInfo()
plan(sequential)