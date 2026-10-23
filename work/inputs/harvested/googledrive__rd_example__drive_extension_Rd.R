# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_extension.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 6

suppressPackageStartupMessages(library(googledrive))
## get the extension for mime type image/jpeg
drive_extension("image/jpeg")

## it's vectorized
drive_extension(c("text/plain", "pdf", "image/gif"))