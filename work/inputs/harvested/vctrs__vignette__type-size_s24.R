# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.R
# lines: 6

suppressPackageStartupMessages(library(vctrs))
x <- sample(1:10)
df <- data.frame(x = x)

vec_slice(x, 5:6)
vec_slice(df, 5:6)