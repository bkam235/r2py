# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_link.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 8

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# get a few files into a dribble
three_files <- drive_find(n_max = 3)

# get their browser links
drive_link(three_files)
}) # examplesIf