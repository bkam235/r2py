# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_token.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 9

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
req <- request_generate(
  "drive.files.get",
  list(fileId = "abc"),
  token = drive_token()
)
req
}) # examplesIf