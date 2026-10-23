# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_compare.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 10

suppressPackageStartupMessages(library(vctrs))
vec_compare(c(TRUE, FALSE, NA), FALSE)
vec_compare(c(TRUE, FALSE, NA), FALSE, na_equal = TRUE)

vec_compare(1:10, 5)
vec_compare(runif(10), 0.5)
vec_compare(letters[1:10], "d")

df <- data.frame(x = c(1, 1, 1, 2), y = c(0, 1, 2, 1))
vec_compare(df, data.frame(x = 1, y = 1))