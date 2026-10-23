# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: sheet_add.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 31

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
ss <- gs4_create("add-sheets-to-me")

# the only required argument is the target spreadsheet
ss %>% sheet_add()

# but you CAN specify sheet name and/or position
ss %>% sheet_add("apple", .after = 1)
ss %>% sheet_add("banana", .after = "apple")

# add multiple sheets at once
ss %>% sheet_add(c("coconut", "dragonfruit"))

# keeners can even specify additional sheet properties
ss %>%
  sheet_add(
    sheet = "eggplant",
    .before = 1,
    gridProperties = list(
      rowCount = 3, columnCount = 6, frozenRowCount = 1
    )
  )

# get an overview of the sheets
sheet_properties(ss)

# clean up
gs4_find("add-sheets-to-me") %>%
  googledrive::drive_trash()
}) # examplesIf