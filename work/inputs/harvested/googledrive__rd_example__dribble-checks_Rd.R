# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: dribble-checks.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 16

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
## most of us have multiple files or folders on Google Drive
d <- drive_find()
is_dribble(d)
no_file(d)
single_file(d)
some_files(d)

# this will error
# confirm_single_file(d)

confirm_some_files(d)
is_folder(d)
is_mine(d)
}) # examplesIf