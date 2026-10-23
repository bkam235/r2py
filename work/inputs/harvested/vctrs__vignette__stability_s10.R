# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: stability_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\stability.R
# lines: 8

suppressPackageStartupMessages(library(vctrs))
try({
c(FALSE, "x")
vec_c(FALSE, "x")

c(FALSE, list(1))
vec_c(FALSE, list(1))
})