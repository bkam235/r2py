# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_libpaths.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 6

suppressPackageStartupMessages(library(withr))
.libPaths()
new_lib <- tempfile()
dir.create(new_lib)
with_libpaths(new_lib, print(.libPaths()))
unlink(new_lib, recursive = TRUE)