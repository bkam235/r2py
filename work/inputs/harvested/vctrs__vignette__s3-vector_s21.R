# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 9

suppressPackageStartupMessages(library(vctrs))
try({
# Correct
c(percent(0.5), 1)
c(percent(0.5), factor(1))

# Incorrect
c(factor(1), percent(0.5))
})