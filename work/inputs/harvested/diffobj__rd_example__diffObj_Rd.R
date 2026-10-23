# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: diffObj.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 4

suppressPackageStartupMessages(library(diffobj))
## `pager="off"` for CRAN compliance; you may omit in normal use
diffObj(letters, c(letters[1:10], LETTERS[11:26]), pager="off")
with(mtcars, diffObj(lm(mpg ~ hp)$qr, lm(mpg ~ disp)$qr, pager="off"))