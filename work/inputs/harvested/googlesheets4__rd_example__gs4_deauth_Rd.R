# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_deauth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 9

suppressPackageStartupMessages(library(googlesheets4))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
gs4_deauth()
gs4_user()

# get metadata on the public 'deaths' spreadsheet
gs4_example("deaths") %>%
  gs4_get()
}) # examplesIf