# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: tibble_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\tibble.R
# lines: 6

suppressPackageStartupMessages(library(tibble))
try({
tibble(a = 1, b = 1:3)
tibble(a = 1:3, b = 1)
tibble(a = 1:3, c = 1:2)
})