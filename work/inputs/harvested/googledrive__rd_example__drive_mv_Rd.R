# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_mv.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 38

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# create a file to move
file <- drive_example_remote("chicken.txt") |>
  drive_cp("chicken-mv.txt")

# rename it, but leave in current folder (root folder, in this case)
file <- drive_mv(file, "chicken-mv-renamed.txt")

# create a folder to move the file into
folder <- drive_mkdir("mv-folder")

# move the file and rename it again,
# specify destination as a dribble
file <- drive_mv(file, path = folder, name = "chicken-mv-re-renamed.txt")

# verify renamed file is now in the folder
drive_ls(folder)

# move the file back to root folder
file <- drive_mv(file, "~/")

# move it again
# specify destination as path with trailing slash
# to ensure we get a move vs. renaming it to "mv-folder"
file <- drive_mv(file, "mv-folder/")

# `overwrite = FALSE` errors if something already exists at target filepath
# THIS WILL ERROR!
drive_create("name-squatter-mv", path = "~/")
drive_mv(file, path = "~/", name = "name-squatter-mv", overwrite = FALSE)

# `overwrite = TRUE` moves the existing item to trash, then proceeds
drive_mv(file, path = "~/", name = "name-squatter-mv", overwrite = TRUE)

# Clean up
drive_rm(file, folder)
}) # examplesIf