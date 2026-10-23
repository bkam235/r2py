# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: range_flood.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 39

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
# create a data frame to use as initial data
df <- gs4_fodder(10)

# create Sheet
ss <- gs4_create("range-flood-demo", sheets = list(df))

# default behavior (`cell = NULL`): clear value and format
range_flood(ss, range = "A1:B3")

# clear value but preserve format
range_flood(ss, range = "C1:D3", reformat = FALSE)

# send new value
range_flood(ss, range = "4:5", cell = ";-)")

# send formatting
# WARNING: use these unexported, internal functions at your own risk!
# This not (yet) officially supported, but it's possible.
blue_background <- googlesheets4:::CellData(
  userEnteredFormat = googlesheets4:::new(
    "CellFormat",
    backgroundColor = googlesheets4:::new(
      "Color",
      red = 159 / 255, green = 183 / 255, blue = 196 / 255
    )
  )
)
range_flood(ss, range = "I:J", cell = blue_background)

# range_clear() is a shortcut where `cell = NULL` always
range_clear(ss, range = "9:9")
range_clear(ss, range = "10:10", reformat = FALSE)

# clean up
gs4_find("range-flood-demo") %>%
  googledrive::drive_trash()
}) # examplesIf