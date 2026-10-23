# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: sheet_rename.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 16

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
ss <- gs4_create(
  "sheet-rename-demo",
  sheets = list(cars = head(cars), chickwts = head(chickwts))
)
sheet_names(ss)

ss %>%
  sheet_rename(1, new_name = "automobiles") %>%
  sheet_rename("chickwts", new_name = "poultry")

# clean up
gs4_find("sheet-rename-demo") %>%
  googledrive::drive_trash()
}) # examplesIf