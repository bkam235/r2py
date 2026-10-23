# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: range_speedread.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 25

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
if (require("readr")) {
  # since cell type is not available, use readr's col type specification
  range_speedread(
    gs4_example("deaths"),
    sheet = "other",
    range = "A5:F15",
    col_types = cols(
      Age = col_integer(),
      `Date of birth` = col_date("%m/%d/%Y"),
      `Date of death` = col_date("%m/%d/%Y")
    )
  )
}

# write a Sheet that, by default, is NOT world-readable
(ss <- sheet_write(chickwts))

# demo that range_speedread() sends a token, which is why we can read this
range_speedread(ss)

# clean up
googledrive::drive_trash(ss)
}) # examplesIf