# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_mime_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 12

suppressPackageStartupMessages(library(googledrive))
## get the mime type for Google Spreadsheets
drive_mime_type("spreadsheet")

## get the mime type for jpegs
drive_mime_type("jpeg")

## it's vectorized
drive_mime_type(c("presentation", "pdf", "image/gif"))

## see the internal tibble of MIME types known to the Drive API
drive_mime_type(expose())