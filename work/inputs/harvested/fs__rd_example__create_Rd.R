# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: create.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 16

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
file_create("foo")
is_file("foo")
# dir_create applied to the same path will fail
try(dir_create("foo"))

dir_create("bar")
is_dir("bar")
# file_create applied to the same path will fail
try(file_create("bar"))

# Cleanup
file_delete("foo")
dir_delete("bar")
setwd(.old_wd)