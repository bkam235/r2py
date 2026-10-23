# r2py crawler metadata
# package: haven
# source_type: rd_example
# topic: read_spss.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\help
# lines: 7

suppressPackageStartupMessages(library(haven))
path <- system.file("examples", "iris.sav", package = "haven")
read_sav(path)

tmp <- tempfile(fileext = ".sav")
write_sav(mtcars, tmp)
read_sav(tmp)