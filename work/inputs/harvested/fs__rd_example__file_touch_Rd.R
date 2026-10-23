# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: file_touch.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 5

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
file_touch("foo", "2018-01-01")
file_info("foo")[c("access_time", "modification_time", "change_time", "birth_time")]
setwd(.old_wd)