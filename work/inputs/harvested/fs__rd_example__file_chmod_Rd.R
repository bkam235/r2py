# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: file_chmod.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 23

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
file_create("foo", mode = "000")
file_chmod("foo", "777")
file_info("foo")$permissions

file_chmod("foo", "u-x")
file_info("foo")$permissions

file_chmod("foo", "a-wrx")
file_info("foo")$permissions

file_chmod("foo", "u+wr")
file_info("foo")$permissions

# It is also vectorized
files <- c("foo", file_create("bar", mode = "000"))
file_chmod(files, "a+rwx")
file_info(files)$permissions

file_chmod(files, c("644", "600"))
file_info(files)$permissions
setwd(.old_wd)