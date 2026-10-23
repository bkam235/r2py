# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: as_dribble.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 18

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# create some files for us to re-discover by name or filepath
alfa <- drive_create("alfa", type = "folder")
bravo <- drive_create("bravo", path = alfa)

# as_dribble() can work with file names or paths
as_dribble("alfa")
as_dribble("bravo")
as_dribble("alfa/bravo")
as_dribble(c("alfa", "alfa/bravo"))

# specify the file id (substitute a real file id of your own!)
# as_dribble(as_id("0B0Gh-SuuA2nTOGZVTXZTREgwZ2M"))

# Clean up
drive_find("alfa") |> drive_rm()
}) # examplesIf