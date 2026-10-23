# r2py crawler metadata
# package: fansi
# source_type: vignette
# topic: sgr-in-rmd_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\doc\sgr-in-rmd.R
# lines: 6

suppressPackageStartupMessages(library(fansi))
try({
message(paste0(sgr.string, collapse="\n"))
warning(paste0(c("", sgr.string), collapse="\n"))
stop(paste0(c("", sgr.string), collapse="\n"))
})