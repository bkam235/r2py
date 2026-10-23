# r2py crawler metadata
# package: prettyunits
# source_type: rd_example
# topic: pretty_sec.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prettyunits\help
# lines: 5

suppressPackageStartupMessages(library(prettyunits))
pretty_sec(c(1337, 13370, 133700, 1337000, 13370000))

pretty_sec(c(1337, 13370, 133700, 1337000, 13370000),
           compact = TRUE)