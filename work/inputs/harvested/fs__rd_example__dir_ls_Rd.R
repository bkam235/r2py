# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: dir_ls.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 21

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
dir_ls(R.home("share"), type = "directory")

# Create a shorter link
link_create(system.file(package = "base"), "base")

dir_ls("base", recurse = TRUE, glob = "*.R")

# If you need the full paths input an absolute path
dir_ls(path_abs("base"))

dir_map("base", identity)

dir_walk("base", str)

dir_info("base")

# Cleanup
link_delete("base")
setwd(.old_wd)