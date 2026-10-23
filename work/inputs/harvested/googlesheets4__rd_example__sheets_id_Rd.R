# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: sheets_id.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 8

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
mini_gap_id <- gs4_example("mini-gap")
class(mini_gap_id)
mini_gap_id

as_sheets_id("abc")
}) # examplesIf