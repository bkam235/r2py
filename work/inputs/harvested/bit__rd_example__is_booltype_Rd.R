# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: is.booltype.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 5

suppressPackageStartupMessages(library(bit))
sapply(
  list(double(), integer(), logical(), bit(), bitwhich(), as.which(), ri(1, 2, 3)),
  is.booltype
)