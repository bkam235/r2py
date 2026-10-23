# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: unit_format.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 6

suppressPackageStartupMessages(library(scales))
# Label with units
demo_continuous(c(0, 1), labels = unit_format(unit = "m"))
# Labels in kg, but original data in g
km <- unit_format(unit = "km", scale = 1e-3, digits = 2)
demo_continuous(c(0, 2500), labels = km)