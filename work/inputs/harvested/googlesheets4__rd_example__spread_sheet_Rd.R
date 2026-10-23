# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: spread_sheet.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 9

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
df <- gs4_example("mini-gap") %>%
  range_read_cells()
spread_sheet(df)

# ^^ gets same result as ...
read_sheet(gs4_example("mini-gap"))
}) # examplesIf