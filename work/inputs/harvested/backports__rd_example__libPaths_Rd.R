# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: libPaths.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 8

suppressPackageStartupMessages(library(backports))
save <- .libPaths()
save
# ignore the site library
.libPaths("test", include.site = FALSE)

# restore the original
.libPaths(save)