# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.R
# lines: 8

suppressPackageStartupMessages(library(vctrs))
try({
# Cast succeeds
vec_cast(c(1, 2), integer())

# Cast fails
vec_cast(c(1.5, 2.5), factor("a"))
})