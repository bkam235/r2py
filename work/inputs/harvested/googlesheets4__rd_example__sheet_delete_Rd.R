# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: sheet_delete.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 20

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
ss <- gs4_create("delete-sheets-from-me")
sheet_add(ss, c("alpha", "beta", "gamma", "delta"))

# get an overview of the sheets
sheet_properties(ss)

# delete sheets
sheet_delete(ss, 1)
sheet_delete(ss, "gamma")
sheet_delete(ss, list("alpha", 2))

# get an overview of the sheets
sheet_properties(ss)

# clean up
gs4_find("delete-sheets-from-me") %>%
  googledrive::drive_trash()
}) # examplesIf