# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: range_read.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 15

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
ss <- gs4_example("deaths")
read_sheet(ss, range = "A5:F15")
read_sheet(ss, range = "other!A5:F15", col_types = "ccilDD")
read_sheet(ss, range = "arts_data", col_types = "ccilDD")

read_sheet(gs4_example("mini-gap"))
read_sheet(
  gs4_example("mini-gap"),
  sheet = "Europe",
  range = "A:D",
  col_types = "ccid"
)
}) # examplesIf