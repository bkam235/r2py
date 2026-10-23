# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: tabs_as_spaces.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 18

suppressPackageStartupMessages(library(fansi))
string <- '1\t12\t123\t1234\t12345678'
tabs_as_spaces(string)
writeLines(
  c(
    '-------|-------|-------|-------|-------|',
    tabs_as_spaces(string)
) )
writeLines(
  c(
    '-|--|--|--|--|--|--|--|--|--|--|',
    tabs_as_spaces(string, tab.stops=c(2, 3))
) )
writeLines(
  c(
    '-|--|-------|-------|-------|',
    tabs_as_spaces(string, tab.stops=c(2, 3, 8))
) )