# r2py crawler metadata
# package: diffobj
# source_type: vignette
# topic: diffobj_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\doc\diffobj.R
# lines: 4

suppressPackageStartupMessages(library(diffobj))
x <- y <- letters[24:26]
y[2] <- "GREMLINS"
diffChr(x, y, mode="unified")