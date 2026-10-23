# r2py crawler metadata
# package: prettyunits
# source_type: rd_example
# topic: pretty_num.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prettyunits\help
# lines: 5

suppressPackageStartupMessages(library(prettyunits))
numbers <- c(1337, 1.3333e-5, 13333337, 1333333337, 133333333337)
pretty_num(numbers)
pretty_num(numbers, style = "nopad")
pretty_num(numbers, style = "6")