# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: sheet_relocate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 33

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
sheet_names <- c("alfa", "bravo", "charlie", "delta", "echo", "foxtrot")
ss <- gs4_create("sheet-relocate-demo", sheets = sheet_names)
sheet_names(ss)

# move one sheet, forwards then backwards
ss %>%
  sheet_relocate("echo", .before = "bravo") %>%
  sheet_names()
ss %>%
  sheet_relocate("echo", .after = "delta") %>%
  sheet_names()

# reorder and move multiple sheets to the front
ss %>%
  sheet_relocate(list("foxtrot", 4)) %>%
  sheet_names()

# put the sheets back in the original order
ss %>%
  sheet_relocate(sheet_names) %>%
  sheet_names()

# reorder and move multiple sheets to the back
ss %>%
  sheet_relocate(c("bravo", "alfa", "echo"), .after = 10) %>%
  sheet_names()

# clean up
gs4_find("sheet-relocate-demo") %>%
  googledrive::drive_trash()
}) # examplesIf