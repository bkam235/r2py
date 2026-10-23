# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 6

suppressPackageStartupMessages(library(S7))
try({
x <- Range(1, 2)
attr(x, "start") <- 3
validate(x)
})