# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_endpoints.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 4

suppressPackageStartupMessages(library(googlesheets4))
str(gs4_endpoints(), max.level = 2)
gs4_endpoints("sheets.spreadsheets.values.get")
gs4_endpoints(4)