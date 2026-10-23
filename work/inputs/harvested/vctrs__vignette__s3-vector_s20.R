# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 12

suppressPackageStartupMessages(library(vctrs))
try({
vec_c(percent(0.5), 1)
vec_c(NA, percent(0.5))
# but
vec_c(TRUE, percent(0.5))

x <- percent(c(0.5, 1, 2))
x[1:2] <- 2:1
x[[3]] <- 0.5
x
})