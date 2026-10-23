# r2py crawler metadata
# package: prettyunits
# source_type: rd_example
# topic: pretty_bytes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prettyunits\help
# lines: 5

suppressPackageStartupMessages(library(prettyunits))
bytes <- c(1337, 133337, 13333337, 1333333337, 133333333337)
pretty_bytes(bytes)
pretty_bytes(bytes, style = "nopad")
pretty_bytes(bytes, style = "6")