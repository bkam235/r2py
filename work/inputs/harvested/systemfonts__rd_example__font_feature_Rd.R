# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: font_feature.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 5

suppressPackageStartupMessages(library(systemfonts))
font_feature(letters = "stylistic", numbers = c("lining", "tabular"))

# Use the tag directly to access additional stylistic variants
font_feature(numbers = c("lining", "tabular"), salt = 2)