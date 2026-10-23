# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: range_read_cells.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 11

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
range_read_cells(gs4_example("deaths"), range = "arts_data")

# if you want detailed and exhaustive cell data, do this
range_read_cells(
  gs4_example("formulas-and-formats"),
  cell_data = "full",
  discard_empty = FALSE
)
}) # examplesIf