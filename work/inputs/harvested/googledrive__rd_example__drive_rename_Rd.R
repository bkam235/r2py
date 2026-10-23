# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_rename.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 19

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Create a file to rename
file <- drive_create("file-to-rename")

# Rename it
file <- drive_rename(file, name = "renamed-file")

# `overwrite = FALSE` errors if something already exists at target filepath
# THIS WILL ERROR!
drive_create("name-squatter-rename")
drive_rename(file, name = "name-squatter-rename", overwrite = FALSE)

# `overwrite = TRUE` moves the existing item to trash, then proceeds
file <- drive_rename(file, name = "name-squatter-rename", overwrite = TRUE)

# Clean up
drive_rm(file)
}) # examplesIf