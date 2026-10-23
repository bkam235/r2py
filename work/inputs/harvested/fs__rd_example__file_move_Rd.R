# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: file_move.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 7

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
file_create("foo")
file_move("foo", "bar")
file_exists(c("foo", "bar"))
file_delete("bar")
setwd(.old_wd)