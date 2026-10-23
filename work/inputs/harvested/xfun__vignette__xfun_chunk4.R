# r2py crawler metadata
# package: xfun
# source_type: vignette
# topic: xfun_chunk4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\doc\xfun.Rmd
# lines: 4

suppressPackageStartupMessages(library(xfun))
f = system.file("LICENSE", package = "xfun")
xfun::file_string(f)
as.character(xfun::file_string(f))  # essentially a character string