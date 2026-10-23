# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_trash.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 17

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Create a file and put it in the trash.
file <- drive_example_remote("chicken.txt") |>
  drive_cp("chicken-trash.txt")
drive_trash("chicken-trash.txt")

# Confirm it's in the trash
drive_find(trashed = TRUE)

# Remove it from the trash and confirm
drive_untrash("chicken-trash.txt")
drive_find(trashed = TRUE)

# Clean up
drive_rm("chicken-trash.txt")
}) # examplesIf