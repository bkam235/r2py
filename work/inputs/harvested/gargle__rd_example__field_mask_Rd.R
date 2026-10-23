# r2py crawler metadata
# package: gargle
# source_type: rd_example
# topic: field_mask.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\help
# lines: 18

suppressPackageStartupMessages(library(gargle))
x <- list(sheetId = 1234, title = "my_favorite_worksheet")
field_mask(x)

x <- list(
  userEnteredFormat = list(
    backgroundColor = list(
      red = 159 / 255, green = 183 / 255, blue = 196 / 255
    )
  )
)
field_mask(x)

x <- list(
  sheetId = 1234,
  gridProperties = list(rowCount = 5, columnCount = 3)
)
field_mask(x)