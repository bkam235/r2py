# r2py crawler metadata
# package: haven
# source_type: rd_example
# topic: read_xpt.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\help
# lines: 4

suppressPackageStartupMessages(library(haven))
tmp <- tempfile(fileext = ".xpt")
write_xpt(mtcars, tmp)
read_xpt(tmp)