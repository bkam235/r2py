# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: sheet_properties.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 6

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
ss <- gs4_example("gapminder")
sheet_properties(ss)
sheet_names(ss)
}) # examplesIf