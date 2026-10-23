# r2py crawler metadata
# package: prettyunits
# source_type: rd_example
# topic: pretty_ms.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prettyunits\help
# lines: 5

suppressPackageStartupMessages(library(prettyunits))
pretty_ms(c(1337, 13370, 133700, 1337000, 1337000000))

pretty_ms(c(1337, 13370, 133700, 1337000, 1337000000),
          compact = TRUE)