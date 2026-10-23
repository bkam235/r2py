# r2py crawler metadata
# package: diffobj
# source_type: vignette
# topic: diffobj_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\doc\diffobj.R
# lines: 4

suppressPackageStartupMessages(library(diffobj))
state.abb2 <- state.abb[-16]
state.abb2[37] <- "Pennsylvania"
diffPrint(state.abb, state.abb2)