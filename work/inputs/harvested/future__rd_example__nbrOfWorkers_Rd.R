# r2py crawler metadata
# package: future
# source_type: rd_example
# topic: nbrOfWorkers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future\help
# lines: 6

suppressPackageStartupMessages(library(future))
plan(multisession)
nbrOfWorkers()  ## == availableCores()

plan(sequential)
nbrOfWorkers()  ## == 1