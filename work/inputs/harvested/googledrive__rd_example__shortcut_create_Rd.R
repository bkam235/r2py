# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: shortcut_create.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 30

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Target one of the official example files
(src_file <- drive_example_remote("chicken_sheet"))

# Create a shortcut in the default location with the default name
sc1 <- shortcut_create(src_file)
# This shortcut could now be moved, renamed, etc.

# Create a shortcut in the default location with a custom name
sc2 <- src_file |>
  shortcut_create(name = "chicken_sheet_second_shortcut")

# Create a folder, then put a shortcut there, with default name
folder <- drive_mkdir("chicken_sheet_shortcut_folder")
sc3 <- src_file |>
  shortcut_create(folder)

# Look at all these shortcuts
(dat <- drive_find("chicken_sheet", type = "shortcut"))

# Confirm the shortcuts all target the original file
dat <- dat |>
  drive_reveal("shortcut_details")
purrr::map_chr(dat$shortcut_details, "targetId")
as_id(src_file)

# Clean up
drive_rm(sc1, sc2, sc3, folder)
}) # examplesIf