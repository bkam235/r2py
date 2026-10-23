# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_id.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 8

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
as_id("123abc")
as_id("https://docs.google.com/spreadsheets/d/qawsedrf16273849/edit#gid=12345")

x <- drive_find(n_max = 3)
as_id(x)
}) # examplesIf