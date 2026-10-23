# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: breaks_extended.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 4

suppressPackageStartupMessages(library(scales))
demo_continuous(c(0, 10))
demo_continuous(c(0, 10), breaks = breaks_extended(3))
demo_continuous(c(0, 10), breaks = breaks_extended(10))