# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: tibble_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\tibble.R
# lines: 8

suppressPackageStartupMessages(library(tibble))
df1 <- data.frame(x = 1:3, y = 3:1)
class(df1[, 1:2])
class(df1[, 1])

df2 <- tibble(x = 1:3, y = 3:1)
class(df2[, 1:2])
class(df2[, 1])