# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_deauth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 11

suppressPackageStartupMessages(library(googledrive))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
drive_deauth()
drive_user()

# in a deauth'ed state, we can still get metadata on a world-readable file
public_file <- drive_example_remote("chicken.csv")
public_file
# we can still download it too
drive_download(public_file)
}) # examplesIf