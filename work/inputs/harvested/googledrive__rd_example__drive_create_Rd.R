# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_create.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 48

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Create a blank Google Doc named 'WordStar' in
# your 'My Drive' root folder and star it
wordstar <- drive_create("WordStar", type = "document", starred = TRUE)

# is 'WordStar' really starred? YES
purrr::pluck(wordstar, "drive_resource", 1, "starred")

# Create a blank Google Slides presentation in
# the root folder, and set its description
execuvision <- drive_create(
  "ExecuVision",
  type = "presentation",
  description = "deeply nested bullet lists FTW"
)

# Did we really set the description? YES
purrr::pluck(execuvision, "drive_resource", 1, "description")

# check out the new presentation
drive_browse(execuvision)

# Create folder 'b4xl' in the root folder,
# then create an empty new Google Sheet in it
b4xl <- drive_mkdir("b4xl")
drive_create("VisiCalc", path = b4xl, type = "spreadsheet")

# Another way to create a Google Sheet in the folder 'b4xl'
drive_create("b4xl/SuperCalc", type = "spreadsheet")

# Yet another way to create a new file in a folder,
# this time specifying parent `path` as a character
drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")

# Did we really create those Sheets in the intended folder? YES
drive_ls("b4xl")

# `overwrite = FALSE` errors if file already exists at target filepath
# THIS WILL ERROR!
drive_create("VisiCalc", path = b4xl, overwrite = FALSE)

# `overwrite = TRUE` moves an existing file to trash, then proceeds
drive_create("VisiCalc", path = b4xl, overwrite = TRUE)

# Clean up
drive_rm(wordstar, b4xl, execuvision)
}) # examplesIf