# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: link_path.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 9

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
file_create("foo")
link_create(path_abs("foo"), "bar")
link_path("bar")

# Cleanup
file_delete(c("foo", "bar"))
setwd(.old_wd)