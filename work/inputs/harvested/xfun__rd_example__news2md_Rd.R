# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: news2md.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
if (interactive()) {
# news for the current version of R
xfun::news2md("R", Version == getRversion(), output = NA)
}