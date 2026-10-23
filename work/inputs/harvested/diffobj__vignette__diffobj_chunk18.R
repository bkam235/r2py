# r2py crawler metadata
# package: diffobj
# source_type: vignette
# topic: diffobj_chunk18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\doc\diffobj.Rmd
# lines: 4

suppressPackageStartupMessages(library(diffobj))
v1 <- 1:5e4
v2 <- v1[-sample(v1, 100)]
diffChr(v1, v2, word.diff=FALSE)