# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_token.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 9

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
req <- request_generate(
  "sheets.spreadsheets.get",
  list(spreadsheetId = "abc"),
  token = gs4_token()
)
req
}) # examplesIf