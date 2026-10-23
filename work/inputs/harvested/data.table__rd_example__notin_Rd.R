# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: notin.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 10

suppressPackageStartupMessages(library(data.table))
11 %notin% 1:10 # TRUE
  "a" %notin% c("a", "b") # FALSE

  ## NAs on the LHS
  NA %in% 1:2
  NA %notin% 1:2
  ## NAs on the RHS
  NA %in% c(1:2,NA)
  NA %notin% c(1:2,NA)