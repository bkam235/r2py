# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: is_file.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 16

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
dir_create("d")

file_create("d/file.txt")
dir_create("d/dir")
link_create(path(path_abs("d"), "file.txt"), "d/link")

paths <- dir_ls("d")
is_file(paths)
is_dir(paths)
is_link(paths)

# Cleanup
dir_delete("d")
setwd(.old_wd)