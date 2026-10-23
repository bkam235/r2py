# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: missing.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 15

suppressPackageStartupMessages(library(vctrs))
x <- c(1, 2, NA, 4, NA)

vec_detect_missing(x)
vec_any_missing(x)

# Data frames are iterated over rowwise, and only report a row as missing
# if every element of that row is missing. If a row is only partially
# missing, it is said to be incomplete, but not missing.
y <- c("a", "b", NA, "d", "e")
df <- data_frame(x = x, y = y)

df$missing <- vec_detect_missing(df)
df$incomplete <- !vec_detect_complete(df)
df