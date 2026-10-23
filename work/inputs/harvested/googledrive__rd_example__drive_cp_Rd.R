# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_cp.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 49

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Target one of the official example files
(src_file <- drive_example_remote("chicken.txt"))

# Make a "Copy of" copy in your My Drive
cp1 <- drive_cp(src_file)

# Make an explicitly named copy, in a different folder, and star it.
# The starring is an example of providing metadata via `...`.
# `starred` is not an actual argument to `drive_cp()`,
# it just gets passed through to the API.
folder <- drive_mkdir("drive-cp-folder")
cp2 <- drive_cp(
  src_file,
  path = folder,
  name = "chicken-cp.txt",
  starred = TRUE
)
drive_reveal(cp2, "starred")

# `overwrite = FALSE` errors if file already exists at target filepath
# THIS WILL ERROR!
# drive_cp(src_file, name = "Copy of chicken.txt", overwrite = FALSE)

# `overwrite = TRUE` moves an existing file to trash, then proceeds
cp3 <- drive_cp(src_file, name = "Copy of chicken.txt", overwrite = TRUE)

# Delete all of our copies and the new folder!
drive_rm(cp1, cp2, cp3, folder)

# Target an official example file that's a csv file
(csv_file <- drive_example_remote("chicken.csv"))

# copy AND AT THE SAME TIME convert it to a Google Sheet
chicken_sheet <- drive_cp(
  csv_file,
  name = "chicken-sheet-copy",
  mime_type = drive_mime_type("spreadsheet")
)
# is it really a Google Sheet?
drive_reveal(chicken_sheet, "mime_type")$mime_type

# go see the new Sheet in the browser
# drive_browse(chicken_sheet)

# Clean up
drive_rm(chicken_sheet)
}) # examplesIf