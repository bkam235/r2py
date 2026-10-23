# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_endpoints.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 4

suppressPackageStartupMessages(library(googledrive))
str(head(drive_endpoints(), 3), max.level = 2)
drive_endpoint("drive.files.delete")
drive_endpoint(4)