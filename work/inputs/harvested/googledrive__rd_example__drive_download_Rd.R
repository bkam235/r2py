# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_download.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 20

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Target one of the official example files
(src_file <- drive_example_remote("chicken_sheet"))

# Download Sheet as csv, explicit type
downloaded_file <- drive_download(src_file, type = "csv")

# See local path to new file
downloaded_file$local_path

# Download as csv, type implicit in file extension
drive_download(src_file, path = "my_csv_file.csv")

# Download with default name and type (xlsx)
drive_download(src_file)

# Clean up
unlink(c("chicken_sheet.csv", "chicken_sheet.xlsx", "my_csv_file.csv"))
}) # examplesIf