# r2py crawler metadata
# package: diffobj
# source_type: vignette
# topic: diffobj_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\doc\diffobj.R
# lines: 6

suppressPackageStartupMessages(library(diffobj))
a <- b <- matrix(1:100, ncol=2)
a <- a[-20,]
b <- b[-45,]
b[c(18, 44)] <- 999
diffPrint(target=a, current=b)