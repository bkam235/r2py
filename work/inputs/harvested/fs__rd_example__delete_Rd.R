# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: delete.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 30

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
# create a directory, with some files and a link to it
dir_create("dir")
files <- file_create(path("dir", letters[1:5]))
link <- link_create(path_abs("dir"), "link")

# All files created
dir_exists("dir")
file_exists(files)
link_exists("link")
file_exists(link_path("link"))

# Delete a file
file_delete(files[1])
file_exists(files[1])

# Delete the directory (which deletes the files as well)
dir_delete("dir")
file_exists(files)
dir_exists("dir")

# The link still exists, but what it points to does not.
link_exists("link")
dir_exists(link_path("link"))

# Delete the link
link_delete("link")
link_exists("link")
setwd(.old_wd)