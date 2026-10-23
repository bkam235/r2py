# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: problems.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 6

suppressPackageStartupMessages(library(readr))
x <- parse_integer(c("1X", "blah", "3"))
problems(x)

y <- parse_integer(c("1", "2", "3"))
problems(y)