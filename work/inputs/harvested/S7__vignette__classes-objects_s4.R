# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 8

suppressPackageStartupMessages(library(S7))
try({
x <- Range(1, 2:3)
x <- Range(10, 1)

x <- Range(1, 10)
x@start <- 20
})