# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_browse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 4

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token() && rlang::is_interactive()) withAutoprint({ # examplesIf
drive_find(n_max = 1) |> drive_browse()
}) # examplesIf