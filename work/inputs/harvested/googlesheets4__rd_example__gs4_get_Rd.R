# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_get.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 4

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
gs4_get(gs4_example("mini-gap"))
}) # examplesIf