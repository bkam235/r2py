# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: range_delete.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 21

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
# create a data frame to use as initial data
df <- gs4_fodder(10)

# create Sheet
ss <- gs4_create("range-delete-example", sheets = list(df))

# delete some rows
range_delete(ss, range = "2:4")

# delete a column
range_delete(ss, range = "C")

# delete a rectangle and specify how to shift remaining cells
range_delete(ss, range = "B3:F4", shift = "left")

# clean up
gs4_find("range-delete-example") %>%
  googledrive::drive_trash()
}) # examplesIf