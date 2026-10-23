# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: sheet_resize.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 30

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
# create a Sheet with the default initial worksheet
(ss <- gs4_create("sheet-resize-demo"))

# see (work)sheet dims
sheet_properties(ss)

# no resize occurs
sheet_resize(ss, nrow = 2, ncol = 6)

# reduce sheet size
sheet_resize(ss, nrow = 5, ncol = 7, exact = TRUE)

# add rows
sheet_resize(ss, nrow = 7)

# add columns
sheet_resize(ss, ncol = 10)

# add rows and columns
sheet_resize(ss, nrow = 9, ncol = 12)

# re-inspect (work)sheet dims
sheet_properties(ss)

# clean up
gs4_find("sheet-resize-demo") %>%
  googledrive::drive_trash()
}) # examplesIf