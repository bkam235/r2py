# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: request_generate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 8

suppressPackageStartupMessages(library(googlesheets4))
req <- request_generate(
  "sheets.spreadsheets.get",
  list(spreadsheetId = gs4_example("deaths")),
  key = "PRETEND_I_AM_AN_API_KEY",
  token = NULL
)
req